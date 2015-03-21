#! /usr/bin/python

import re
import codecs
import urllib
import binascii
import os
import pickle
import sys

homedir = os.path.split( os.path.realpath( sys.argv[0] ) )[0]

bo_dict = pickle.load(open(os.path.join(homedir, "pinyin_bopomofo_dictionary")))

# regular expressions used in parsing -- these have been extensively
# tested and should gracefully handle all the HTML variants that
# show up on ChinesePod

# for each tab, there is one regular expression to extract sentences,
# and another regular expression to parse the sentence -- in theory,
# these regular expressions could be combined, but in practice, this
# doesn't work, as overly complicated regular expressions are horribly
# inefficient, especially for scanning such large HTML files, and
# therefore sometimes don't terminate

# these might not be entirely comprehensible; sorry!

break_word = re.compile(r"(?P<punct>[^&<>;/]+)|(<span.*?event, ?'\s*(?P<literal>.*?)\s*','\s*(?P<pinyin>.*?)\s*','\s*(?P<trad>.*?)\s*','\s*(?P<simp>.*?)\s*'.*?/span>)")

break_dialogue = re.compile(r'<button.*?</button>.*?</div>.*?</div>', flags = re.DOTALL)
break_dialogue_sentence = re.compile(r'<button.*?url=(?P<mp3>.*?\.mp3).*?</button.*?(?P<speaker>\w?):(&nbsp;)*\s*(?P<words>.*?)\s*(</div>|<br/>.*?(<span\ id=.*?>(?P<idiomatic>.*?)</span>)+.*?</div>)', flags = re.DOTALL)

break_expansion = re.compile(r'(<h6>.*?</h6>)|(<button.*?</button>.*?</div>.*?</p>)', flags = re.DOTALL)
break_expansion_sentence = re.compile(r'(<h6>(?P<exp>.*?)</h6>)|(<button.*?url=(?P<mp3>.*?\.mp3).*?</button>.*?</div>\s*(?P<words>.*?)\s*<br />.*?(</p>|<span\ id=.*?>(?P<idiomatic>.*?)</span>))', flags = re.DOTALL)

break_vocab = re.compile(r'(?P<switch>Supplementary Vocab)|(vocab\[].*?<button.*?url=.*?\.mp3)', flags = re.DOTALL)
break_vocab_sentence = re.compile(r'(?P<switch>Supplementary Vocab)|(vocab\[].*?&nbsp;\s*(?P<trad>[ \S]+?)\s*?</label>.*?<td.*?>(?P<pinyin>.*?)</td>.*?<td.*?>(?P<literal>.*?)</td>.*?<button.*?url=(?P<mp3>.*?\.mp3))', flags = re.DOTALL)

find_esc_unicode = re.compile(r'&#(?P<code>\d+);')
find_syllable = re.compile(r'\w+?\d')

get_title = re.compile('<h1><a href.*?>(?P<level>.*?)</a> -\s*(?P<name>.*?)\s*</h1>')
get_desc = re.compile('<meta name="description" content="\s*(?P<desc>.*?)\s*"', flags = re.DOTALL)
get_image = re.compile('"Lesson Picture" src="\s*(?P<img>.*?)\s*"')

xml_header = '<?xml version="1.0" encoding="utf-8"?>\n<?xml-stylesheet type="text/xsl" href="wlcpod.xsl"?>\n'

# translation table for converting from tone-numbered pinyin to tone-marked

ends_in = [u'v1', u'v2', u'v3', u'v4', u'v5', u've1', u've2', u've3', u've4', u've5', u'vn1', u'vn2', u'vn3', u'vn4', u'vn5', u'a1', u'a2', u'a3', u'a4', u'a5', u'ai1', u'ai2', u'ai3', u'ai4', u'ai5', u'an1', u'an2', u'an3', u'an4', u'an5', u'ao1', u'ao2', u'ao3', u'ao4', u'ao5', u'ang1', u'ang2', u'ang3', u'ang4', u'ang5', u'e1', u'e2', u'e3', u'e4', u'e5', u'en1', u'en2', u'en3', u'en4', u'en5', u'er1', u'er2', u'er3', u'er4', u'er5', u'eng1', u'eng2', u'eng3', u'eng4', u'eng5', u'ei1', u'ei2', u'ei3', u'ei4', u'ei5', u'i1', u'i2', u'i3', u'i4', u'i5', u'in1', u'in2', u'in3', u'in4', u'in5', u'ing1', u'ing2', u'ing3', u'ing4', u'ing5', u'o1', u'o2', u'o3', u'o4', u'o5', u'ou1', u'ou2', u'ou3', u'ou4', u'ou5', u'ong1', u'ong2', u'ong3', u'ong4', u'ong5', u'u1', u'u2', u'u3', u'u4', u'u5', u'ue1', u'ue2', u'ue3', u'ue4', u'ue5', u'ui1', u'ui2', u'ui3', u'ui5', u'un1', u'un2', u'un3', u'un4', u'un5']

ends_out = [u'\u01d6', u'\u01d8', u'\u01da', u'\u01dc', u'\xfc', u'\u01d6e', u'\u01d8e', u'\u01dae', u'\u01dce', u'\xfce', u'\u01d6n', u'\u01d8n', u'\u01dan', u'\u01dcn', u'\xfcn', u'\u0101', u'\xe1', u'\u01ce', u'\xe0', u'a', u'\u0101i', u'\xe1i', u'\u01cei', u'\xe0i', u'ai', u'\u0101n', u'\xe1n', u'\u01cen', u'\xe0n', u'an', u'\u0101o', u'\xe1o', u'\u01ceo', u'\xe0o', u'ao', u'\u0101ng', u'\xe1ng', u'\u01ceng', u'\xe0ng', u'ang', u'\u0113', u'\xe9', u'\u011b', u'\xe8', u'e', u'\u0113n', u'\xe9n', u'\u011bn', u'\xe8n', u'en', u'\u0113r', u'\xe9r', u'\u011br', u'\xe8r', u'er', u'\u0113ng', u'\xe9ng', u'\u011bng', u'\xe8ng', u'eng', u'\u0113i', u'\xe9i', u'\u011bi', u'\xe8i', u'ei', u'\u012b', u'\xed', u'\u01d0', u'\xec', u'i', u'\u012bn', u'\xedn', u'\u01d0n', u'\xecn', u'in', u'\u012bng', u'\xedng', u'\u01d0ng', u'\xecng', u'ing', u'\u014d', u'\xf3', u'\u01d2', u'\xf2', u'o', u'\u014du', u'\xf3u', u'\u01d2u', u'\xf2u', u'ou', u'\u014dng', u'\xf3ng', u'\u01d2ng', u'\xf2ng', u'ong', u'\u016b', u'\xfa', u'\u01d4', u'\xf9', u'u', u'\u016be', u'\xfae', u'\u01d4e', u'\xf9e', u'ue', u'\u016bi', u'\xfai', u'\u01d4i', u'uie', u'\u016bn', u'\xfan', u'\u01d4n', u'\xf9n', u'un']

def get_bopomofos(pinyin):
	"""tries to produce the bopomofo corresponding to a string of
	tone-numbered pinyin"""

	def add_e(s):
		if len(s) == 2 and s[0] == 'r':
			return 'e' + s

		return s

	try:
		return [bo_dict[add_e(i).replace('5', '').lower()] for i in find_syllable.findall(pinyin)]
	except:
		return []

def word_xml(word, word2, indent):
	"""generates XML for a Chinese word;
		word: a regex match object representing a word
		word2: another match object providing a simplified equivalent
			if necessary
		indent: XML indentation"""

	if word2 is None and word.group('punct') is not None:
		return indent + '<punctuation>%s</punctuation>\n' % word.group('punct')

	def char_xml(trad, simp, bopos, indent = ''):
		# append big5/unicode codes for each character -- please test! (some characters, such as u'\u88cf', don't seem to convert)
		def hex_big5(c):
			try:
				return binascii.hexlify(c.encode('big5'))
			except:
				return ''

		def esc_big5(c):
			try:
				return urllib.quote(c.encode('big5'))
			except:
				return ''

		return ''.join([indent.join(['',
			'<character>\n',
			'\t<traditional>%s</traditional>\n' % n,
			'\t<simplified>%s</simplified>\n' % m,
			'\t<bopomofo>%s</bopomofo>\n' % p,
			'\t<hex-big5>%s</hex-big5>\n' % hex_big5(n),
			'\t<esc-big5>%s</esc-big5>\n' % esc_big5(n),
			'</character>\n']) for n,m,p in zip(trad, simp, bopos)])

	if word2 is None:
		def tone_mark_unicode(pinyin):
			for n,m in zip(ends_in, ends_out):
				pinyin = pinyin.replace(n,m)
			return pinyin

	else:
		def tone_mark_unicode(pinyin):
			return find_esc_unicode.sub(lambda p: unichr(int(p.group('code'))), pinyin)

	# insert mp3 info if it exists
	try:
		mp3 = '%s\t<mp3>%s</mp3>\n' % (indent, os.path.split(word.group('mp3'))[1])
	except:
		mp3 = ''

	# set up bopomofos
	bopos = []
	bopos += get_bopomofos(word.group('pinyin'))
	bopos += [' '] * (len(word.group('trad')) - len(bopos))

	return indent.join(['',
		'<word>\n' + mp3,
		'\t<literal>%s</literal>\n' % word.group('literal'),
		'\t<pinyin>%s</pinyin>\n' % tone_mark_unicode(word.group('pinyin')),
		'\t<esc-unicode>%s</esc-unicode>\n' % urllib.quote(word.group('trad').encode('utf-8')) +
		char_xml(word.group('trad'), word2 and word2.group('trad') or word.group('simp'), bopos, indent + '\t'),
		'</word>\n'])

def dialogue_xml(html, indent, mp3s):
	"""generates XML for a dialogue section of a lesson;
		html: the HTML representing a dialogue tab in traditional mode
		indent: XML indentation
		mp3s: a list to be filled in with mp3 filenames"""

	def sentence_xml(sentence, indent = ''):

		old = sentence
		sentence = break_dialogue_sentence.search(sentence.group())

		if sentence is None:
			print "funny HTML encountered (dialogue)"
			return ""

		mp3s.append(sentence.group('mp3'))

		return indent.join(['',
			'<sentence>\n',
			'\t<mp3>%s</mp3>\n' % os.path.split(sentence.group('mp3'))[1],
			'\t<idiomatic>%s</idiomatic>\n' % sentence.group('idiomatic'),
			'\t<speaker>%s</speaker>\n' % sentence.group('speaker') +
			''.join([word_xml(word, None, indent + '\t') for word in break_word.finditer(sentence.group('words'))]),
			'</sentence>\n'])

	return '%s<dialogue_sentences>\n%s%s</dialogue_sentences>\n' % (indent,
		'\n'.join([sentence_xml(sentence, indent + '\t') for sentence in break_dialogue.finditer(html)]),
		indent)

def expansion_xml(html, indent, mp3s):
	"""generates XML for an expansion section of a lesson;
	html: the HTML representing an expansion tab in traditional mode
	indent: XML indentation
	mp3s: a list to be filled in with mp3 filenames"""

	def sentence_xml(sentence, indent = ''):
		old = sentence
		sentence = break_expansion_sentence.search(sentence.group())

		if sentence is None:
			print "funny HTML encountered (expansion)"
			return ""

		if sentence.group('exp') is not None:
			return indent + '<expansion_word>%s</expansion_word>\n' % sentence.group('exp')

		mp3s.append(sentence.group('mp3'))

		return indent.join(['',
			'<sentence>\n',
			'\t<mp3>%s</mp3>\n' % os.path.split(sentence.group('mp3'))[1],
			'\t<idiomatic>%s</idiomatic>\n' % sentence.group('idiomatic') +
			''.join([word_xml(word, None, indent + '\t') for word in break_word.finditer(sentence.group('words'))]),
			'</sentence>\n'])

	return '%s<expansion_sentences>\n%s%s</expansion_sentences>\n' % (indent,
		'\n'.join([sentence_xml(sentence, indent + '\t') for sentence in break_expansion.finditer(html)]),
		indent)

def vocabulary_xml(trad_html, simp_html, indent, mp3s):
	"""generates XML for a vocabulary section of a lesson;
	trad_html: the HTML representing an expansion tab in traditional mode
	simp_html: as above, but in traditional mode
	indent: XML indentation
	mp3s: a list to be filled in with mp3 filenames"""

	# check for duplicates
	last_def = ['']

	def line_xml(trad, simp, last_def, indent = ''):
		trad_old = trad
		simp_old = simp

		trad = break_vocab_sentence.search(trad.group())
		simp = break_vocab_sentence.search(simp.group())

		if trad is None or simp is None:
			print "funny HTML encountered (vocab)"
			return ""

		if trad.group('switch') is not None:
			return indent.join(['',
				'</key_vocabulary>\n\n',
				'<supplementary_vocabulary>\n'])

		# skip if this is a duplicate
		if last_def[0] == trad.group('trad'):
			return ''
		else:
			last_def[0] = trad.group('trad')

		mp3s.append(trad.group('mp3'))
		return word_xml(trad, simp, indent + '\t')

	return indent.join(['',
		'<key_vocabulary>\n' +
		''.join([line_xml(n,m,last_def,indent) for n,m in zip(break_vocab.finditer(trad_html), break_vocab.finditer(simp_html))]),
		'%s\n' % ('Supplementary Vocab' in trad_html and '</supplementary_vocabulary>' or '</key_vocabulary>')])

def lesson_params(html):
	"""returns the base URL for downloading premium content, as well
	as the lesson id, title/difficulty level and description"""

	title = (lambda x: '%s (%s)' % (x.group('name'), x.group('level')))(get_title.search(html))
	desc = get_desc.search(html).group('desc')
	base_url = get_image.search(html).group('img').replace('images','%s').replace('.jpg','%s')

	return title, desc, base_url

def lesson_xml(id, vocab_trad_html, vocab_simp_html, dia_html, exp_html, disc_html):
	"""returns lesson xml, as well as mp3s needed by the
	Vocabulary, Dialogue and Expansion tabs and a base URL for
	downloading lesson MP3s and PDFs;
	id: the lesson id (as in the URLs)
	*.html: the tab HTML files downloaded from ChinesePod"""
			
	vocab_mp3s, dia_mp3s, exp_mp3s = [], [], []

	title, desc, base_url = lesson_params(disc_html)

	lesson_xml = (xml_header
		+ '<lesson>\n'
		+ '\t<id>%s</id>\n' % id
		+ '\t<esc-esc-id>%s</esc-esc-id>\n' % urllib.quote(id.encode('utf-8')).replace('%', '%25')
		+ '\t<title_and_level>%s</title_and_level>\n' % title
		+ '\t<desc>%s</desc>\n\n' % desc
		+ vocabulary_xml(vocab_trad_html, vocab_simp_html, '\t', vocab_mp3s)
		+ '\n'
		+ dialogue_xml(dia_html, '\t', dia_mp3s)
		+ '\n'
		+ expansion_xml(exp_html, '\t', exp_mp3s)
		+ '</lesson>\n').replace('\\\'', '\'')

        #DerekChadwick: replace invalid XML character, using &amp; created valid XML but displayed &amp; instead of &
        lesson_xml = lesson_xml.replace("&", "and")
        
	return title, desc, base_url, lesson_xml, vocab_mp3s, dia_mp3s, exp_mp3s
