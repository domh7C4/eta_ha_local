// SPDX-License-Identifier: GPL-3.0-only
// ETA Heating Card 1.0.1. No dashboards, sidebar panels or writes on rendering.
(() => {
  function buildConfig(config, states) {
    const matches = Object.values(states).filter(state =>
      state.attributes.eta_integration === "eta_readonly" &&
      (!config.config_entry_id || state.attributes.eta_config_entry_id === config.config_entry_id));
    const sensors = matches.filter(s => s.entity_id.startsWith("sensor.")).sort((a,b) => a.entity_id.localeCompare(b.entity_id));
    const controls = matches.filter(s => s.entity_id.startsWith("select.") && s.attributes.write_access_enabled);
    const temps = sensors.filter(s => s.attributes.device_class === "temperature");
    const cards = [];
    if (config.title) cards.push({type:"markdown", content:"## " + config.title});
    if (sensors.length) {
      const preferred = config.picture_entity && sensors.find(s => s.entity_id === config.picture_entity);
      cards.push({type:"picture-entity", entity:(preferred || temps[0] || sensors[0]).entity_id,
        image:"/eta_readonly/eta-logo.png", fit_mode:"contain", aspect_ratio:"16:9",
        show_name:true, show_state:true, tap_action:{action:"more-info"}});
      cards.push({type:"entities", title:"Heizungswerte", show_header_toggle:false,
        entities:sensors.map(s => ({entity:s.entity_id}))});
      if (config.show_history !== false && temps.length) cards.push({type:"history-graph",
        title:"Temperaturverlauf", hours_to_show:24, entities:temps.map(s => s.entity_id)});
    } else cards.push({type:"markdown",content:"Keine passenden ETA-Sensoren gefunden. Integration einrichten oder die Anlagen-ID im Karteneditor prüfen."});
    if (config.show_controls !== false && controls.length) cards.push({type:"entities",title:"Heizungssteuerung",
      show_header_toggle:false,entities:controls.map(s => ({entity:s.entity_id}))});
    cards.push({type:"markdown", content:"Unabhängige, inoffizielle Integration. ETA-Name und -Logo gehören den jeweiligen Rechteinhabern."});
    return {type:"vertical-stack",cards};
  }

  class EtaHeatingCard extends HTMLElement {
    constructor() { super(); this.attachShadow({mode:"open"}); this._serial = 0; }
    static getStubConfig() { return {type:"custom:eta-heating-card",title:"ETA Heizung",show_history:true,show_controls:true}; }
    static getConfigElement() { return document.createElement("eta-heating-card-editor"); }
    setConfig(config) {
      this._config = {...EtaHeatingCard.getStubConfig(), ...config};
      this._signature = null;
      this._update();
    }
    set hass(hass) { this._hass = hass; if (this._card) this._card.hass = hass; this._update(); }
    getCardSize() { return 12; }
    getGridOptions() { return {columns:12, min_columns:6}; }
    async _update() {
      if (!this._config || !this._hass) return;
      const cfg = buildConfig(this._config, this._hass.states || {});
      const signature = JSON.stringify(cfg);
      if (signature === this._signature) return;
      this._signature = signature;
      const serial = ++this._serial;
      try {
        const helpers = await window.loadCardHelpers();
        if (serial !== this._serial) return;
        const card = helpers.createCardElement(cfg);
        card.hass = this._hass;
        this._card = card;
        this.shadowRoot.replaceChildren(card);
      } catch (err) {
        if (serial !== this._serial) return;
        this._signature = null;
        const message = document.createElement("ha-card");
        message.textContent = "ETA-Karte konnte nicht geladen werden: " + err.message;
        this.shadowRoot.replaceChildren(message);
      }
    }
  }

  class EtaHeatingCardEditor extends HTMLElement {
    constructor() { super(); this.attachShadow({mode:"open"}); }
    setConfig(config) { this._config = {...EtaHeatingCard.getStubConfig(), ...config}; this._render(); }
    set hass(hass) { this._hass = hass; }
    _render() {
      if (!this._config) return;
      const form = document.createElement("div"); form.style.display="grid"; form.style.gap="16px";
      const field = (key,label) => {
        const input = document.createElement("ha-textfield"); input.label=label; input.value=this._config[key] || "";
        input.addEventListener("change", () => this._change(key,input.value)); form.append(input);
      };
      field("title","Titel");
      field("config_entry_id","Anlagen-ID (optional, leer = alle ETA-Anlagen)");
      field("picture_entity","Bild-Sensor (optional, z. B. sensor.kesseltemperatur)");
      for (const [key,label] of [["show_history","Temperaturverlauf anzeigen"],["show_controls","Heizungssteuerung anzeigen"]]) {
        const line=document.createElement("label"); line.style.display="flex"; line.style.alignItems="center"; line.style.gap="12px";
        const toggle=document.createElement("ha-switch"); toggle.checked=this._config[key] !== false;
        toggle.addEventListener("change",()=>this._change(key,toggle.checked));
        const text=document.createElement("span"); text.textContent=label; line.append(toggle,text); form.append(line);
      }
      this.shadowRoot.replaceChildren(form);
    }
    _change(key,value) {
      this._config={...this._config,[key]:value};
      this.dispatchEvent(new CustomEvent("config-changed",{detail:{config:this._config},bubbles:true,composed:true}));
    }
  }
  if (!customElements.get("eta-heating-card")) customElements.define("eta-heating-card",EtaHeatingCard);
  if (!customElements.get("eta-heating-card-editor")) customElements.define("eta-heating-card-editor",EtaHeatingCardEditor);
  window.customCards = window.customCards || [];
  if (!window.customCards.some(card => card.type === "eta-heating-card")) window.customCards.push({
    type:"eta-heating-card",name:"ETA Heizung Lokal",description:"ETA-Logo, automatisch erkannte Sensoren, Temperaturverlauf und freigegebene Steuerung.",preview:true});
})();
