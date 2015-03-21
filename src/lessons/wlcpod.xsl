<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<!-- WLCP 2009.03.22 XSLT stylesheet; jwlee -->
<!-- <xsl:output method="html" encoding="utf-8"
	doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN"
	doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"/> -->
<xsl:output method="html" encoding="utf-8"
	doctype-public="-//W3C//DTD HTML 4.0 Transitional//EN"
	doctype-system="http://www.w3.org/TR/REC-html40/loose.dtd"/>

<xsl:template match="traditional|simplified|literal|title_and_level|idiomatic">
  <xsl:value-of select="normalize-space(.)"/>
</xsl:template>

<xsl:template match="punctuation">
	<word class="tooltip"><chinese-text>
		<xsl:value-of select="normalize-space(.)"/>
	</chinese-text></word>

	<word class="annotate annt">
	<table>
	<tr><td><xsl:text>&#160;&#160;</xsl:text></td></tr>

	<tr><td>
	<chinese-text>
		<xsl:value-of select="normalize-space(.)"/>
	</chinese-text>
	</td></tr>

	<tr><td><xsl:text>&#160;&#160;</xsl:text></td></tr>
	</table>
	</word>
	</xsl:template>

<xsl:template match="pinyin">
	<xsl:if test="position()!=1"><xsl:text> </xsl:text></xsl:if>
	<xsl:value-of select="normalize-space(.)"/>
</xsl:template>

<xsl:template match="expansion_word">
	<h3><xsl:value-of select="normalize-space(.)"/></h3>
</xsl:template>
 
<xsl:template match="speaker">
	<strong><xsl:value-of select="normalize-space(.)"/>: </strong>
</xsl:template>

<xsl:template match="idiomatic">
	<idiomatic><xsl:value-of select="normalize-space(.)"/></idiomatic>
</xsl:template>

<xsl:template match="word">
	<xsl:param name = "vocab">0</xsl:param>

	<word class='tooltip'>
	<chinese-text>
		<trad><xsl:for-each select="character"><xsl:value-of select="normalize-space(traditional)"/></xsl:for-each></trad>
		<simp><xsl:for-each select="character"><xsl:value-of select="normalize-space(simplified)"/></xsl:for-each></simp>
	</chinese-text>
	<tip>
		<tooltip-trad>
			<xsl:apply-templates select=".//traditional"/>
		</tooltip-trad>

		<tooltip-simp><xsl:text>（</xsl:text>

		<xsl:apply-templates select=".//simplified"/>
		<xsl:text>）</xsl:text></tooltip-simp>

		<p><xsl:apply-templates select=".//pinyin"/><br/>
		<xsl:apply-templates select="literal"/></p>

		<p>
		<xsl:text>TMOE stroke look-up: </xsl:text>
		<xsl:for-each select="character">
			<xsl:if test="position()!=1"><xsl:text>, </xsl:text></xsl:if>
			<a href="http://stroke-order.learningweb.moe.edu.tw/word_detail.jsp?big5={normalize-space(hex-big5)}">
			<xsl:apply-templates select="traditional"/></a>
		</xsl:for-each>
		<br/>

		<xsl:text>CUHK character look-up: </xsl:text>
		<xsl:for-each select="character">
			<xsl:if test="position()!=1"><xsl:text>, </xsl:text></xsl:if>
			<a href="http://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/search.php?q={normalize-space(esc-big5)}">
			<xsl:apply-templates select="traditional"/></a>
		</xsl:for-each>

		<br/>
		<xsl:text>CantoDict character look-up: </xsl:text>
		<a href="http://www.cantonese.sheik.co.uk/dictionary/search/?searchtype=1&amp;text={normalize-space(esc-unicode)}"><xsl:apply-templates select=".//traditional"/></a>
		</p>
	</tip>
	</word>

	<xsl:choose><xsl:when test="$vocab = 1">
	<word class='plain'>
	<chinese-text>
		<trad><xsl:for-each select="character"><xsl:value-of select="normalize-space(traditional)"/></xsl:for-each></trad>
		<simp><xsl:for-each select="character"><xsl:value-of select="normalize-space(simplified)"/></xsl:for-each></simp>
	</chinese-text>
	</word>
	</xsl:when>

	<xsl:otherwise>
	<word class='pinyin-annotate annt'>
	<table>
	<caption><xsl:value-of select="literal"/></caption>
	<tr><td class='pinyin-annt'><xsl:text>&#160;&#160;</xsl:text>
		<xsl:value-of select="pinyin"/>
	<xsl:text>&#160;&#160;</xsl:text></td></tr>

	<tr><td>
	<chinese-text>
		<trad><xsl:for-each select="character"><xsl:value-of select="normalize-space(traditional)"/></xsl:for-each></trad>
		<simp><xsl:for-each select="character"><xsl:value-of select="normalize-space(simplified)"/></xsl:for-each></simp>
	</chinese-text>
	</td></tr>
	</table>
	</word>

	<word class='bopomofo-annotate annt'>
	<table>
	<caption><xsl:value-of select="literal"/></caption>

	<tr><xsl:for-each select="character">
		<td class='bopomofo-annt'><xsl:value-of select="normalize-space(bopomofo)"/></td>
	</xsl:for-each></tr>

	<tr><xsl:for-each select="character">
		<td><chinese-text>
			<trad><xsl:value-of select="normalize-space(traditional)"/></trad>
			<simp><xsl:value-of select="normalize-space(simplified)"/></simp>
		</chinese-text></td>
	</xsl:for-each></tr>
	</table>
	</word>
	</xsl:otherwise></xsl:choose>
</xsl:template>

<xsl:template match="sentence">
	<p>
		<table>
		<tr>
		<td class='no-print col'><object type="application/x-shockwave-flash" data="player_mp3_maxi.swf" width="190" height="20">
			<param name="movie" value="player_mp3_maxi.swf" />
			<param name="bgcolor" value="#ff0000" />
			<param name="FlashVars" value="mp3={normalize-space(//esc-esc-id)}/{normalize-space(mp3)}&amp;showslider=1&amp;width=190" />
		</object></td>
		<td class='text'><xsl:apply-templates select="speaker"/>
		<xsl:apply-templates select="word|punctuation"/></td>
		</tr>

		<tr><td class='no-print'></td>
		<td class='pinyin'>
			<xsl:for-each select="punctuation|word"><xsl:choose>
			<xsl:when test="name(.) = 'punctuation'">
				<xsl:value-of select="translate(normalize-space(.),'？。！','?.!')"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:if test="position() != 1"><xsl:text> </xsl:text></xsl:if>
				<xsl:value-of select=".//pinyin"/>
			</xsl:otherwise>
			</xsl:choose></xsl:for-each>
		</td></tr>

		<tr><td class='no-print'></td>
		<td class='semantic'><xsl:apply-templates select="idiomatic"/>
		</td></tr>
		</table>
</p>
</xsl:template>

<xsl:template match="key_vocabulary | supplementary_vocabulary">
	<p><table>
		<xsl:for-each select="word">
			<tr>
			<td class='no-print col'><object type="application/x-shockwave-flash" data="player_mp3_maxi.swf" width="190" height="20">
				<param name="movie" value="player_mp3_maxi.swf" />
				<param name="bgcolor" value="#ff0000" />
				<param name="FlashVars" value="mp3={normalize-space(//esc-esc-id)}/{normalize-space(mp3)}&amp;showslider=1&amp;width=190" />
			</object></td>
			<td class='col'><xsl:apply-templates select="."><xsl:with-param name = "vocab">1</xsl:with-param></xsl:apply-templates></td>
			<td class='col'><xsl:apply-templates select=".//pinyin"/></td>
			<td><xsl:apply-templates select="literal"/></td>
			</tr>
		</xsl:for-each>
	</table></p>
</xsl:template>

<xsl:template match="/">
	<html>
	<head>
		<link rel="stylesheet" type="text/css" href="wlcpod.css" /> 
		<title><xsl:apply-templates select="lesson/title_and_level"/> - WLCP</title>
	</head>
	<body>

	<script language="JavaScript" type="text/javascript" src="wlcpod.js" />
	<xsl:for-each select="lesson">
		<h1><xsl:apply-templates select="title_and_level"/>
		<xsl:text> - </xsl:text>
		<a href="http://wlcp.googlecode.com/">WLCP</a></h1>

		<xsl:text>ChinesePod lesson webpage: </xsl:text><a href="http://www.chinesepod.com/lessons/{normalize-space(id)}">http://www.chinesepod.com/lessons/<xsl:value-of select="normalize-space(id)"/></a>
		<noprint>
		<br/>
		<xsl:text>Master list of WLCP-downloaded lessons: </xsl:text>
		<a href="wlcpod-master-index.xml">wlcpod-master-index.xml</a>
		</noprint>
		<br/><br/>
		<table>
		<tr>
		<td class='col'><img align="left" src="{normalize-space(id)}/{normalize-space(id)}.jpeg"/></td>
		<td><xsl:value-of select="normalize-space(desc)"/></td>
		</tr>
		</table>

		<noprint>
		<p>
		<table>
		<tr><td class='col'>
			<object type="application/x-shockwave-flash" data="player_mp3_maxi.swf" width="190" height="20" id="myFlash">
			<param name="movie" value="player_mp3_maxi.swf" />
			<param name="bgcolor" value="#ff0000" />
			<param name="FlashVars" value="mp3={normalize-space(esc-esc-id)}/{normalize-space(esc-esc-id)}_lesson.mp3" />
			</object></td>

		<td class='col'><a href="{normalize-space(id)}/{normalize-space(id)}_lesson.mp3">Lesson MP3</a></td>
		
		<td><xsl:text>Traditional lesson transcripts: </xsl:text>
		<a href="{normalize-space(id)}/{normalize-space(id)}-trad.pdf">PDF</a>
		<xsl:text>/</xsl:text>
		<a href="{normalize-space(id)}/{normalize-space(id)}-trad.html">HTML</a></td></tr>

		<tr><td>
			<object type="application/x-shockwave-flash" data="player_mp3_maxi.swf" width="190" height="20">
			<param name="movie" value="player_mp3_maxi.swf" />
			<param name="bgcolor" value="#ff0000" />
			<param name="FlashVars" value="mp3={normalize-space(esc-esc-id)}/{normalize-space(esc-esc-id)}_dialogue.mp3" />
			</object></td>
		<td><a href="{normalize-space(id)}/{normalize-space(id)}_dialogue.mp3">Dialogue MP3</a></td>
		
		<td><xsl:text>Simplified lesson transcripts: </xsl:text>
		<a href="{normalize-space(id)}/{normalize-space(id)}-simp.pdf">PDF</a>
		<xsl:text>/</xsl:text>
		<a href="{normalize-space(id)}/{normalize-space(id)}-simp.html">HTML</a></td></tr>


		<tr><td>
			<object type="application/x-shockwave-flash" data="player_mp3_maxi.swf" width="190" height="20">
			<param name="movie" value="player_mp3_maxi.swf" />
			<param name="bgcolor" value="#ff0000" />
			<param name="FlashVars" value="mp3={normalize-space(esc-esc-id)}/{normalize-space(esc-esc-id)}_review.mp3" />
			</object></td>
		<td><a href="{normalize-space(id)}/{normalize-space(id)}_review.mp3">Audio review MP3</a></td></tr>
		<tr><td>
			<object type="application/x-shockwave-flash" data="player_mp3_maxi.swf" width="190" height="20">
			<param name="movie" value="player_mp3_maxi.swf" />
			<param name="bgcolor" value="#ff0000" />
			<param name="FlashVars" value="mp3={normalize-space(esc-esc-id)}/{normalize-space(esc-esc-id)}_expansion_sentences.mp3" />
			</object></td>
		<td><a href="{normalize-space(id)}/{normalize-space(id)}_review.mp3">Expansion MP3</a></td></tr>
		<tr><td>
			<object type="application/x-shockwave-flash" data="player_mp3_maxi.swf" width="190" height="20">
			<param name="movie" value="player_mp3_maxi.swf" />
			<param name="bgcolor" value="#ff0000" />
			<param name="FlashVars" value="mp3={normalize-space(esc-esc-id)}/{normalize-space(esc-esc-id)}_vocabulary_sentences.mp3" />
			</object></td>
		<td><a href="{normalize-space(id)}/{normalize-space(id)}_review.mp3">Vocabulary MP3</a></td></tr>
		</table>
		</p>

		<h2>WLCP Settings</h2>

		<ul><li><input type='button' onclick='toggleCharType()' value='Toggle'/> Character mode: <strong id='charType'>traditional</strong></li>

		<li><input type='button' onclick='toggleText()' value='Toggle'/> Chinese sentences: <strong id='text'>shown</strong></li>

		<li><input type='button' onclick='toggleSemantic()' value='Toggle'/> English semantic sentence translations: <strong id='semantic'>shown</strong></li>

		<li><input type='button' onclick='togglePinyin()' value='Toggle'/> Pinyin sentence translations: <strong id='pinyin'>hidden</strong></li>

		<li><input type='button' onclick='toggleTooltip()' value='Toggle'/> Extra word information: <strong id='tooltip'>tooltips</strong></li>

		<li><input type='button' onclick='noPrint()' value='Make page suitable for printing'/></li>
		</ul>

		<a href="http://wlcp.googlecode.com/">WLCP</a>
		<xsl:text> needs your help gaining support! Please consider helping spread the word about it.</xsl:text>
		</noprint>

		<xsl:for-each select="key_vocabulary">
			<h2>Key Vocabulary</h2>
			<xsl:apply-templates select="."/>
		</xsl:for-each>

		<xsl:for-each select="supplementary_vocabulary">
			<h2>Supplementary Vocabulary</h2>
			<xsl:apply-templates select="."/>
		</xsl:for-each>

		<xsl:for-each select="dialogue_sentences">
			<h2>Dialogue</h2>
			<xsl:apply-templates select="sentence"/>
		</xsl:for-each>

		<xsl:for-each select="expansion_sentences">
			<h2>Expansion</h2>
			<xsl:apply-templates select="sentence|expansion_word"/>
		</xsl:for-each>
	</xsl:for-each>

	<br/><br/><br/><br/>
	</body>
	</html>
</xsl:template>

</xsl:stylesheet>

