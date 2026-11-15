// SPDX-License-Identifier: GPL-3.0-only
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
class Element {
  attachShadow(){ this.shadowRoot={children:[],replaceChildren(...nodes){this.children=nodes}}; }
}
const registry=new Map();
const context={HTMLElement:Element,customElements:{get:key=>registry.get(key),define:(key,value)=>registry.set(key,value)},
  window:{customCards:[],loadCardHelpers:async()=>({createCardElement:cfg=>({cfg})})},
  document:{createElement:()=>({})}};
vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../custom_components/eta_readonly/www/eta-heating-card.js'),'utf8'),context);
const Card=registry.get('eta-heating-card');
const state=(entity_id,extra={})=>({entity_id,state:'40',attributes:{eta_integration:'eta_readonly',eta_config_entry_id:'boiler1',...extra}});
const states={'sensor.status':state('sensor.status'),'sensor.temp':state('sensor.temp',{device_class:'temperature'}),
  'sensor.foreign':{entity_id:'sensor.foreign',state:'1',attributes:{}},
  'select.mode':state('select.mode',{write_access_enabled:true}),
  'sensor.second':state('sensor.second',{eta_config_entry_id:'boiler2'})};
const tick=()=>new Promise(resolve=>setImmediate(resolve));
async function render(config={},data=states){const card=new Card();card.setConfig(config);card.hass={states:data};await tick();return card;}
(async()=>{
  let card=await render();let cards=card._card.cfg.cards;
  assert.equal(cards.find(c=>c.type==='picture-entity').entity,'sensor.temp');
  assert.equal(cards.find(c=>c.type==='picture-entity').image,'/eta_readonly/eta-logo.png');
  assert(!JSON.stringify(cards).includes('sensor.foreign'));
  assert(cards.some(c=>c.title==='Heizungssteuerung'));
  card=await render({config_entry_id:'boiler1'});assert(!JSON.stringify(card._card.cfg).includes('sensor.second'));
  card=await render({show_history:false,show_controls:false,picture_entity:'sensor.status'});cards=card._card.cfg.cards;
  assert(!cards.some(c=>c.type==='history-graph'||c.title==='Heizungssteuerung'));
  assert.equal(cards.find(c=>c.type==='picture-entity').entity,'sensor.status');
  card=await render({},{});assert(!card._card.cfg.cards.some(c=>c.type==='picture-entity'));
  card=await render();const original=card._card;card.hass={states};await tick();assert.equal(card._card,original);
  assert.equal(context.window.customCards[0].type,'eta-heating-card');
  console.log('6 card checks passed: discovery, instance filtering, controls/history settings, empty state, live update reuse, card picker.');
})().catch(err=>{console.error(err);process.exitCode=1});
