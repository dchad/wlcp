<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<!-- <xsl:output method="html" encoding="utf-8"
	doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN"
	doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"/> -->
<xsl:output method="html" encoding="utf-8"
	doctype-public="-//W3C//DTD HTML 4.0 Transitional//EN"
	doctype-system="http://www.w3.org/TR/REC-html40/loose.dtd"/>

<xsl:template name="strip" match="traditional|simplified|literal|pinyin|
	punctuation|title_and_level|idiomatic">
  <xsl:value-of select="normalize-space(.)"/>
</xsl:template>

<xsl:template match="/"><xsl:for-each select="index">
	<html>
	<head>
		<link rel="stylesheet" type="text/css" href="wlcpod.css" /> 
		<title>WLCP Lesson Index</title>
	</head>
	<body>

	<h1>WLCP Lesson Index</h1>

	<xsl:for-each select="lesson">
		<h2><xsl:apply-templates select="title_and_level"/></h2>

		<a href="{normalize-space(id)}.xml"><xsl:value-of select="normalize-space(id)"/>.xml</a>
		<br/><br/>
		<table>
		<tr>
		<td class='col'><img align="left" src="{normalize-space(id)}/{normalize-space(id)}.jpeg"/></td>
		<td><xsl:value-of select="normalize-space(desc)"/></td>
		</tr>
		</table>
	</xsl:for-each>

	<br/><br/><br/><br/>
	</body>
	</html>
</xsl:for-each></xsl:template>

</xsl:stylesheet>

