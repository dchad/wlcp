/* WLCP 2009.03.22 (jwlee) -- JavaScript backend for display toggling buttons */

/* status */
var modeTraditional = 1
var modeSemantic = 1
var modePinyin = 0
var modeText = 1
var modeTooltip = 0

var rules = document.styleSheets[0].cssRules

function setDisplay(selector, display) {
	for(var i=0; i<rules.length; i++) {
		if(rules[i].selectorText == selector) {
			rules[i].style.display = display
		}
	}
}

function toggleCharType() {
	if(modeTraditional == 1) {
		modeTraditional = 0
		document.getElementById('charType').innerHTML = 'simplified'
		setDisplay('chinese-text trad', 'none')
		setDisplay('chinese-text simp', 'inline')
	} else {
		modeTraditional = 1
		document.getElementById('charType').innerHTML = 'traditional'
		setDisplay('chinese-text trad', 'inline')
		setDisplay('chinese-text simp', 'none')
	}
}

function toggleSemantic() {
	if(modeSemantic == 1) {
		modeSemantic = 0
		document.getElementById('semantic').innerHTML = 'hidden'
		setDisplay('td.semantic', 'none')
	} else {
		modeSemantic = 1
		document.getElementById('semantic').innerHTML = 'shown'
		setDisplay('td.semantic', 'inline')
	}
}

function togglePinyin() {
	if(modePinyin == 1) {
		modePinyin = 0
		document.getElementById('pinyin').innerHTML = 'hidden'
		setDisplay('td.pinyin', 'none')
	} else {
		modePinyin = 1
		document.getElementById('pinyin').innerHTML = 'shown'
		setDisplay('td.pinyin', 'inline')
	}
}

function toggleText() {
	if(modeText == 1) {
		modeText = 0
		document.getElementById('text').innerHTML = 'hidden'
		setDisplay('td.text', 'none')
	} else {
		modeText = 1
		document.getElementById('text').innerHTML = 'shown'
		setDisplay('td.text', 'inline')
	}
}

function toggleTooltip() {
	if(modeTooltip == 2) {
		modeTooltip = 0
		document.getElementById('tooltip').innerHTML = 'tooltips'
		setDisplay('word.tooltip', 'inline')
		setDisplay('word.plain', 'none')
		setDisplay('word.annotate', 'none')
		setDisplay('word.bopomofo-annotate', 'none')
	} else if (modeTooltip == 0) {
		modeTooltip = 1
		document.getElementById('tooltip').innerHTML = 'annotations (with pinyin)'
		setDisplay('word.tooltip', 'none')
		setDisplay('word.plain', 'inline')
		setDisplay('word.annotate', 'inline')
		setDisplay('word.pinyin-annotate', 'inline')
	} else {
		modeTooltip = 2
		document.getElementById('tooltip').innerHTML = 'annotations (with bopomofo)'
		setDisplay('word.pinyin-annotate', 'none')
		setDisplay('word.bopomofo-annotate', 'inline')
	}
}

function noPrint() {
	setDisplay('td.no-print', 'none')
	setDisplay('noprint', 'none')
	setDisplay('word:hover tip', 'none')
}
