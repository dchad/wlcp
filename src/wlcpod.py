#!/usr/bin/python
# -*- coding: utf-8 -*-


version = u'2009.09.12'
copyright_and_disclaimer = \
u"""-----------------------------------------------------------------------
We Love ChinesePod! version: %s, default encoding: %s
Copyright 2008 Andrew Corrigan under the GPL v3
http://wlcp.googlecode.com/
-----------------------------------------------------------------------
"""
"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
-----------------------------------------------------------------------
"""

# configuration settings
config = None
	
import sys
import codecs
import urllib, urllib2
import os
import pickle
import ConfigParser
import re
import shutil

#DerekChadwick : get WLCP home directory and current working directory so WLCP can be run from any directory
homedir = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
current_working_dir = os.getcwd()
print 'WLCP Home directory: %s' % homedir
print 'Current working directory: %s' % current_working_dir

#DerekChadwick: find broken URLs on the CPOD web pages, when the URL string ends up with a bunch of html in it, then this causes urllib.retrieve() to bail out!
find_broken_url = re.compile(r'<.*</')
#DerekChadwick: Checks for valid newbie, elementary, intermediate, upper-intermediate, advanced and media mp3 files to confirm if the page is a main lesson and not an extra lesson.
mp3_regex = re.compile('chinesepod_([A-Z]*)([0-9]{4})pb.mp3')
#DerekChadwick: fixes for cpods file name changes
lesson_file_name = re.compile('chinesepod_([A-Z]*)([0-9]{4})')
pdf_simp_file_name = re.compile('chinesepod_([A-Z]*)([0-9]{4}).pdf')
pdf_trad_file_name = re.compile('chinesepod_([A-Z]*)([0-9]{4})trad.pdf')


from wlcpod_netops import (cpod_login, download_file, get_html, cpod_trad, cpod_simp)
from wlcpod_parser import lesson_xml
from xml.dom.minidom import Document

def skip_past(html, marker, start=0): return html.index(marker,start)+len(marker)

def pinyin_latex(pinyin_tone_number):
	s = pinyin_tone_number.strip()
	if(len(s) > 1) and s[0:2] == "ng":
		return s

	unicodes = u"ǖǘǚǜüāáǎàēéěèīíǐìōóǒòūúǔù"
	out = u"\\" + s.replace("Long", "LONG").replace("long", "Long")

	try:
		int(out[len(out) - 1])
	except:
		out = out + "5"

	return out

def convert_to_html(unicode):
	return urllib.quote(unicode.encode('utf-8')).replace('%', '%25')

def break_up(pinyin, pinyins=None):
	if pinyins is None: pinyins = []
	index = 0
	for i in range(len(pinyin)):
		try: tone = int(pinyin[i])
		except: continue
		pinyins.append(pinyin[index:i+1].replace(u'5',u'').lower())
		index = i+1
	if index < len(pinyin): pinyins.append(pinyin[index:len(pinyin)].replace(u'5',u'').lower())
	return pinyins

def main():
	# Redirect output to a log file for debugging purposes
	class RedirectOutput:
		def __init__(self, stdout, log):
			self.stdout = stdout
			self.log = log
			self.tab = 0

		def write(self, s):
			self.stdout.write(s.encode('utf-8'))
			self.log.write(s)

	# configuration settings along with defaults
	global config
	config = ConfigParser.ConfigParser({
		'language' : 'chinese',
		'logfile' : 'welovechinesepodlog.txt',
		'lessondir' : 'lessons',
		'lessonfile' : 'lessons.txt',
		'downloaded-lessons-file' : 'downloaded-lessons.txt',
		'index-file' : 'wlcpod-index.xml',
		'master-index-file' : 'wlcpod-master-index.xml',
                'support-files' : 'player_mp3_maxi.swf wlcpod.css wlcpod.js wlcpod.xsl wlcpod-index.xsl wlcpod-latex.xsl wlcpod-latex.sh',
		'get-lesson-mp3s' : 'yes',
		'get-dialogue-mp3s' : 'yes',
		'get-review-mp3s' : 'yes',
		'get-expansion-sentence-mp3s' : 'yes',
		'get-dialogue-sentence-mp3s' : 'yes',
		'get-vocabulary-sentence-mp3s' : 'yes',
		'get-traditional-pdf' : 'yes',
		'get-simplified-pdf' : 'no',
		'cache-unparsed': 'yes',
		'cachedir' : 'cache',
		'listdirs': 'no',
		'old-pinyin-behaviour': 'no'
	})
	config.read(os.path.join(homedir, "wlcpod.ini"))

	lessondir = config.get('welovechinesepod', 'lessondir')
	cachedir = config.get('welovechinesepod', 'cachedir')
	#DerekChadwick: added current working lesson directory
	cwd_lesson_dir = os.path.join(current_working_dir, lessondir)
		
	# set up logging
	log = codecs.open(config.get('welovechinesepod','logfile'), 'w', 'utf-8')
	sys_stdout = sys.stdout
	sys_stderr = sys.stderr
	redirected_output = RedirectOutput(sys_stdout, log)
	sys.stdout = redirected_output
	sys.stderr = redirected_output

	print copyright_and_disclaimer % (version, sys.getdefaultencoding())

	# bopomofo conversion
	# log.write(u'loading pinyin-bopomofo dictionary\n')
	# bo_dict = pickle.load(open('pinyin_bopomofo_dictionary'))

	# create cache directory
	if config.getboolean('welovechinesepod', 'cache-unparsed'):
		try:
			os.mkdir(cachedir)
		except OSError, (errno, strerror):
			if errno == 17 or errno == 183: log.write(u'The folder ' + cachedir + u' already exists; no need to create.\n')
			else: raise OSError(errno, strerror)

	# create lesson directory
	try:
		os.mkdir(cwd_lesson_dir)
	except OSError, (errno, strerror):
		if errno == 17 or errno == 183: log.write(u'The folder ' + cwd_lesson_dir + u' already exists\n')
		else: raise OSError(errno, strerror) 

	# master downloaded lessons log
	downloaded_lessons_filename = os.path.join(cwd_lesson_dir, config.get('welovechinesepod', 'downloaded-lessons-file'))
	try:
		downloaded_lessons_log = codecs.open(downloaded_lessons_filename, 'r', 'utf-8')
		downloaded_lessons, downloaded_lesson_titles, downloaded_lesson_descs = [list(i) for i in zip(*[l.strip().split('###') for l in downloaded_lessons_log])]
		downloaded_lessons_log.close()
	except:
		downloaded_lessons, downloaded_lesson_titles, downloaded_lesson_descs = [], [], []

	# lessons downloaded from this session
	session_lessons, session_lesson_titles, session_lesson_descs = [], [], []
	
	downloaded_lessons_log = codecs.open(downloaded_lessons_filename, 'a', 'utf-8')

	# login information
	try:
		email = config.get('welovechinesepod', 'email')
		password = config.get('welovechinesepod', 'password')

	except:
		print 'No login information was found in wlcpod.ini!  Requesting it now...'
		email = unicode(raw_input(u'\tYour email address: '), 'utf-8')
		password = unicode(raw_input(u'\tYour password: '), 'utf-8')

	# lesson information	
	# DerekChadwick: added home directory path to lesson file name so WLCP can be run from any directory
	try:
		lessonfile = config.get('welovechinesepod', 'lessonfile')
		lesson_names = [lesson_name.strip() for lesson_name in codecs.open(os.path.join(homedir, lessonfile), 'r', 'utf-8').readlines() if lesson_name.strip() is not '']			
		print 'Successfully read %s lesson name(s) (from %s to %s) from the file %s.' % (len(lesson_names), lesson_names[0], lesson_names[-1], lessonfile)

	except:
		print 'No lesson name not found in %s!  Requesting it now...' % lessonfile
		lesson_names = [unicode(raw_input(u'\tLesson name, exactly as it appears in the URL: '), 'utf-8').strip()]
		log.write('user entered lesson %s\n' % lesson_names[0])

	# language information
	language = config.get('welovechinesepod', 'language')

	# login to Praxis [language]Pod!
	cpod_login(email, password)

	for lesson_index, lesson_name in enumerate(lesson_names):
		if len(lesson_name) < 1: continue
		if lesson_name[0] == u'\ufeff':
			lesson_name = lesson_name[1:]
			print u'ignoring first byte of lesson_name %d' % lesson_index
			if len(lesson_name) < 1: continue

		# skip lesson names starting with a *
		if lesson_name[0] == '*':
			continue

		print u'\n\n%s\nDownloading lesson %d/%d: "%s"\n\tto folder %s\n%s' % (50 * '=', lesson_index+1, len(lesson_names), lesson_name, os.path.join(cwd_lesson_dir, lesson_name), 50 * '=')

		# create a folder to hold the files 
		try:
			os.mkdir(os.path.join(cwd_lesson_dir, lesson_name))
		except OSError, (errno, strerror):
			if errno == 17 or errno == 183:
				log.write(u'The folder ' + os.path.join(cwd_lesson_dir, lesson_name) + u' already exists\n')
			else: raise OSError(errno, strerror) 
			
		already_existing_files = os.listdir(os.path.join(cwd_lesson_dir, lesson_name))

		if config.getboolean('welovechinesepod', 'listdirs'):
			print 'Folder contents:'
			for name in already_existing_files:
				print u'\t' + name

		# download lesson tab HTML		
		print 'Downloading lesson HTML data...'
		base_tab_url = 'http://%spod.com/lessons/%s/%%s' % (language, urllib.quote_plus(lesson_name.encode('utf-8')).replace('%', '%%'))
		base_localname = os.path.join(cachedir, '%s_%%s.html' % lesson_name)

		if config.getboolean('welovechinesepod', 'cache-unparsed'):
			caching = True
		else:
			caching = False

		# download tabs
		vocab_simp = get_html(base_tab_url % 'vocabulary', caching and base_localname % 'vocab_simp' or None, ctype='simp')
		vocab_trad = get_html(base_tab_url % 'vocabulary', caching and base_localname % 'vocab_trad' or None, ctype='trad')
		dia_trad = get_html(base_tab_url % 'dialogue', caching and base_localname % 'dia_trad' or None, ctype='trad')
		exp_trad = get_html(base_tab_url % 'expansion', caching and base_localname % 'exp_trad' or None, ctype='trad')
		disc_trad = get_html(base_tab_url % 'discussion', caching and base_localname % 'disc_trad' or None, ctype='trad')

		#DerekChadwick: added checking of return document, if it is None then the lesson name is probably bad, so skip to the next lesson
		#Note: the cpod server returns a "Pay Up" page instead of a HTTP error for non-existent expansion, dialogue pages for the extra lessons,
		#So use a regex to search for valid main lesson mp3s to determine if this is a valid lesson page, this seems to be the only safe way to check...
		
		if disc_trad == None or mp3_regex.search(disc_trad) == None:
			print 'ERROR: Lesson (%s) could not be downloaded, skipping to next lesson.' % lesson_name
			continue

		if vocab_simp == vocab_trad:
			print "identical simp and trad"

		# parse it!
		title_and_level, lesson_desc, base_url, xml, vocab_mp3s, dia_mp3s, exp_mp3s = lesson_xml(lesson_name, vocab_trad, vocab_simp, dia_trad, exp_trad, disc_trad)

		# save the XML document
		xml_filename = os.path.join(cwd_lesson_dir, lesson_name) + u'.xml'
		print u'Saving XML document as %s...' % xml_filename
		f = codecs.open(xml_filename, 'w', 'utf-8')
		f.write(xml)
		f.close()

		# download other (non-sentence MP3) media
		#DerekChadwick: added fixes supplied by Jon for downloading the simp and trad html.
		#DerekChadwick: cpods file naming has gone all over the place like a mad dogs breakfast...
		print 'Downloading image, selected PDFs and main lesson MP3s...'

                mp3_search_result = mp3_regex.search(disc_trad)
                if mp3_search_result == None:
                        print 'ERROR2: Lesson (%s) could not be downloaded, skipping to next lesson.' % lesson_name
                        continue
                
                lesson_main_file_name_search = lesson_file_name.search(disc_trad)
		if lesson_main_file_name_search == None:
                        print 'ERROR3: MP3 files for lesson (%s) could not be downloaded, skipping to next lesson.' % lesson_name
                        continue
                
                lesson_main_file_name_base = lesson_main_file_name_search.group()
               
		pdf_file_name_search = pdf_simp_file_name.search(disc_trad)
		if pdf_file_name_search == None:
                        pdf_file_name_search = pdf_trad_file_name.search(disc_trad)
                        if pdf_file_name_search == None:
                                print 'ERROR4: PDF files for lesson (%s) could not be downloaded, skipping to next lesson.' % lesson_name
                                continue
                        else:
                                pdf_base = pdf_file_name_search.group()
                                pdf_file_name_base = pdf_base[0:pdf_base.rfind('trad')]
                else:
                        pdf_base = pdf_file_name_search.group()
                        pdf_file_name_base = pdf_base[0:pdf_base.rfind('.pdf')]
                        
		last_fslash = base_url.rfind('/')
                image_file_name = base_url[last_fslash+1:len(base_url)]
		lesson_base_url = base_url[0:last_fslash+1]
		
		image_url = base_url % ('images', '.jpg')
		simp_pdf_url = lesson_base_url % ('pdf') + pdf_file_name_base + '.pdf'
		trad_pdf_url = lesson_base_url % ('pdf') + pdf_file_name_base + 'trad.pdf'
		simp_html_url = lesson_base_url % ('pdf') + pdf_file_name_base + '.html'
                trad_html_url = lesson_base_url % ('pdf') + pdf_file_name_base + 'trad.html'
		podcast_url = lesson_base_url % ('mp3') + lesson_main_file_name_base + 'pr.mp3'
		dialogue_url = lesson_base_url % ('mp3') + lesson_main_file_name_base + 'dg.mp3'
		review_url = lesson_base_url % ('mp3') + lesson_main_file_name_base + 'rv.mp3'

		image_filename = lesson_name + u'.jpeg'
		simp_pdf_filename = lesson_name + u'-simp.pdf'
		trad_pdf_filename = lesson_name + u'-trad.pdf'
		simp_html_filename = lesson_name + u'-simp.html'
                trad_html_filename = lesson_name + u'-trad.html'
		podcast_filename = lesson_name + u'_lesson.mp3'
		dialogue_filename = lesson_name + u'_dialogue.mp3'
		review_filename = lesson_name + u'_review.mp3'

		# download the image!
		download_file(cwd_lesson_dir, lesson_name, image_filename, image_url, already_existing_files)

		# download simplified transcript
		if config.getboolean('welovechinesepod', 'get-simplified-pdf'):
			download_file(cwd_lesson_dir, lesson_name, simp_pdf_filename, simp_pdf_url, already_existing_files)

		# download traditional transcript
		if config.getboolean('welovechinesepod', 'get-traditional-pdf'):
			download_file(cwd_lesson_dir, lesson_name, trad_pdf_filename, trad_pdf_url, already_existing_files)
			
                # download simplified transcript (HTML)
                if config.getboolean('welovechinesepod', 'get-simplified-html'):
                        download_file(cwd_lesson_dir, lesson_name, simp_html_filename, simp_html_url, already_existing_files)

                # download traditional transcript (HTML)
                if config.getboolean('welovechinesepod', 'get-traditional-html'):
                        download_file(cwd_lesson_dir, lesson_name, trad_html_filename, trad_html_url, already_existing_files)

		# download podcast mp3
		if config.getboolean('welovechinesepod', 'get-lesson-mp3s'):
			download_file(cwd_lesson_dir, lesson_name, podcast_filename, podcast_url, already_existing_files)

		# download dialogue mp3
		if config.getboolean('welovechinesepod', 'get-dialogue-mp3s'):
			download_file(cwd_lesson_dir, lesson_name, dialogue_filename, dialogue_url, already_existing_files)

		# download review MP3s
		if config.getboolean('welovechinesepod', 'get-review-mp3s'):
			download_file(cwd_lesson_dir, lesson_name, review_filename, review_url, already_existing_files)

		# download the sentence MP3s
		for tab, mp3s in zip(["vocabulary", "dialogue", "expansion"], [vocab_mp3s, dia_mp3s, exp_mp3s]):
			if not config.getboolean('welovechinesepod', 'get-' + tab + '-sentence-mp3s'):
				continue

			print u'Downloading %d %s sentences...' % (len(mp3s), tab)

			# DerekChadwick: added URL validation and some more path goodness
			names = []
			for url, name in zip(mp3s, [os.path.split(url)[1] for url in mp3s]):
				if name is '' or find_broken_url.search(url) != None:
					print '\tERROR: Skipping mp3 with bad URL: %s' % url
					continue
				else:
					download_file(cwd_lesson_dir, lesson_name, name, url, already_existing_files, names)


			names_and_silence = []
			for name in names:
				if tab == u'expansion':
					names_and_silence.append(os.path.join(cwd_lesson_dir, lesson_name) + u'/' + name)
					names_and_silence.append(os.path.join(homedir, u'silence3_5.mp3'))
				if tab == u'vocabulary':
					names_and_silence.append(os.path.join(cwd_lesson_dir, lesson_name) + u'/' + name)
					names_and_silence.append(os.path.join(homedir, u'silence2.mp3'))
				names_and_silence.append(os.path.join(cwd_lesson_dir, lesson_name) + u'/' + name)
				names_and_silence.append(os.path.join(homedir, u'silence2.mp3'))

			# combine each of the mp3 files into one file
			mp3_filename = lesson_name + u'_' + tab + u'_sentences' + u'.mp3'
			if mp3_filename in already_existing_files:
				print mp3_filename + u' already exists!'
			else:
				print u'Combining MP3 files into %s...' % mp3_filename
				output_song = open(os.path.join(cwd_lesson_dir, lesson_name + u'/' + mp3_filename), 'wb')
				for f in names_and_silence: output_song.write(open(f, 'rb').read())

		# update the log
		if lesson_name not in downloaded_lessons:
			downloaded_lessons.append(lesson_name)
			downloaded_lesson_titles.append(title_and_level)
			downloaded_lesson_descs.append(lesson_desc)

			downloaded_lessons_log.write(lesson_name + u'###' + title_and_level + u'###' + lesson_desc.replace('\n', ' ') + u'\n')
			downloaded_lessons_log.flush()

		# lessons from this session
		if lesson_name not in session_lessons:
			session_lessons.append(lesson_name)
			session_lesson_titles.append(title_and_level)
			session_lesson_descs.append(lesson_desc)

		# redirected_output.decrease_tab()
		print u'Finished with lesson: %s' % lesson_name 
		print u'=' * 50

	# create and save the index XML document for this session
	def write_lesson_index(lessons, titles, descs, filename):
		xml = ''.join(['<?xml version="1.0" encoding="utf-8"?>\n',
			'<?xml-stylesheet type="text/xsl" href="wlcpod-index.xsl"?>\n',
			'<index>\n',
			''.join(['\t'.join(['',
				'<lesson>\n',
				'\t<id>%s</id>\n' % id,
				'\t<title_and_level>%s</title_and_level>\n' % title,
				'\t<desc>%s</desc>\n' % desc,
				'</lesson>\n']) for id, title, desc in zip(lessons, titles, descs)]),
			'</index>\n'])

		codecs.open(xml_filename, u'w', encoding='utf-8').write(xml)

	xml_filename = os.path.join(cwd_lesson_dir, config.get('welovechinesepod', 'index-file'))

	print u'Saving XML index of lesson(s) just downloaded as %s...' % xml_filename
	write_lesson_index(session_lessons, session_lesson_titles, session_lesson_descs, xml_filename)

	xml_filename = os.path.join(cwd_lesson_dir, config.get('welovechinesepod', 'master-index-file'))
	print u'Saving XML index of all lessons ever downloaded as %s...' % xml_filename
	write_lesson_index(downloaded_lessons, downloaded_lesson_titles, downloaded_lesson_descs, xml_filename)
	
	#DerekChadwick: copy the xsl/css files to the lesson directory if the current working directory is not the WLCP directory
	home_lesson_dir = os.path.join(homedir, lessondir)
		
	if home_lesson_dir != cwd_lesson_dir:
                for fname in config.get('welovechinesepod', 'support-files').split(' '):
                        shutil.copy(os.path.join(home_lesson_dir, fname), cwd_lesson_dir)

if __name__ == '__main__':
	main()

