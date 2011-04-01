#!/usr/bin/env python
import sys
import re
import datetime
import urllib
import os
try:
	import wikipydia
except ImportError:
	sys.path.append('/home/bahn/work/wikipydia')
	import wikipydia

def convert_topics(filename, lang):
	date = None
	topics_re = re.compile(r'^([0-9]{4})-([0-9]{2})-([0-9]{2})\.topics$')
	m = topics_re.match(os.path.basename(filename))
	if m:
		date = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

	lineno = 0
	with open(filename, 'r') as f:
		topics = read_lines_from_file(sys.argv[1])
		topic_line_re1 = re.compile("^(.+) ([0-9]+)$")
		topic_line_re2 = re.compile("^([^\t]+)\t([0-9]+)$")
		print "<table>";
		print "<tr><th>Rank</th><th>Titles and links</th><th>Trending score</th></tr>";
		for line in f:
			lineno += 1
			line = line.rstrip('\n')
			m = topic_line_re1.match(line)
			if m:
				title = m.group(1)
				pageviews = m.group(2)
			else:
				m = topic_line_re2.match(line)
				if m:
					title = m.group(1)
					pageviews = m.group(2)
				else:
					title = line
					pageviews = None
			title = title.decode('utf8')
			if not wikipydia.query_exists(title, lang):
				continue
			title = wikipydia.query_redirects(title, lang)
			title = title.encode('utf8')
			if date:
				oldid = str(wikipydia.query_revid_by_date(title, lang, date))
			escaped_title = urllib.quote(title.encode('utf8').replace(' ','_'), safe="") # force / to be quoted
			print '<tr><td>%d</td><td>%s <a href="http://%s.wikipedia.org/wiki/%s" target="view">[now]</a>' % (lineno, title, lang, escaped_title),
			if date:
				pass
				print ' <a href="http://' + lang + '.wikipedia.org/w/index.php?title=' + escaped_title + '&oldid=' + oldid + '" target="viewthen">[then]</a>',
			if lang != 'en':
				print ' <a href="http://translate.google.com/translate?hl=en&sl=' + lang + '&tl=en&u=http%3A%2F%2F' + lang + '.wikipedia.org%2Fwiki%2F' + escaped_title + '" target="translate">[now:translate]</a>',
				if date:
					pass
					print ' <a href="http://translate.google.com/translate?hl=en&sl=' + lang + '&tl=en&u=http%3A%2F%2F' + lang + '.wikipedia.org%2Fw%2Findex.php?title=' + escaped_title + '&oldid=' + oldid + '" target="translatethen">[then:translate]</a>',
			if pageviews:
				pass
				print "</td><td>%d" % (pageviews),
			print "</td></tr>";
		print "</table>";

if __name__=='__main__':
	lang = 'en'
	while len(sys.argv) > 1 and sys.argv[1].startswith('-'):
		if len(sys.argv) > 2 and sys.argv[1] == '-l':
			lang = sys.argv[2]
			sys.argv[1:3] = []
		else:
			sys.stderr.write('Unknown switch: %s\n' % sys.argv[1])
			sys.exit(1)
	if len(sys.argv) != 2:
		sys.stderr.write('Usage: %s [-l LANG] FILE\n' % sys.argv[0])
		sys.exit(1)
	filename = sys.argv[1]
	convert_topics(filename, lang)
