<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" encoding="utf-8" />

<xsl:template name="strip" match="traditional|simplified|literal|latex-pinyin|
	punctuation|title_and_level|lesson_id|idiomatic|speaker|idiomatic">
  <xsl:value-of select="normalize-space(.)"/>
</xsl:template>

<xsl:template name="word-trad">
	<xsl:apply-templates select=".//traditional"/>
	<xsl:apply-templates select="punctuation"/>
</xsl:template>

<xsl:template name="word-simp">
	<xsl:apply-templates select=".//simplified"/>
	<xsl:apply-templates select="punctuation"/>
</xsl:template>

<xsl:template name="word-pinyin">
	<xsl:apply-templates select=".//latex-pinyin"/>
	<xsl:for-each select="punctuation">
		<xsl:value-of select="translate(normalize-space(.),'？。！','?.!')"/>
	</xsl:for-each>
</xsl:template>

<xsl:template name="diagitem">
	<xsl:text>\diagitem{</xsl:text>
	<xsl:apply-templates select="speaker"/>
	<xsl:text>}{</xsl:text>

	<xsl:for-each select="word">
		<xsl:call-template name="word-trad"/>
	</xsl:for-each>
	<xsl:text>}{</xsl:text>

	<xsl:for-each select="word">
		<xsl:call-template name="word-simp"/>
	</xsl:for-each>
	<xsl:text>}{</xsl:text>

	<xsl:for-each select="word">
		<xsl:if test="position()!=1"><xsl:text> </xsl:text></xsl:if>
		<xsl:call-template name="word-pinyin"/>
	</xsl:for-each>
	<xsl:text>}{</xsl:text>

	<xsl:apply-templates select="idiomatic"/>
	<xsl:text>}
</xsl:text>
</xsl:template>

<xsl:template match="sentence">
	<xsl:text>\expitem{</xsl:text>

	<xsl:for-each select="word">
		<xsl:call-template name="word-trad"/>
	</xsl:for-each>
	<xsl:text>}{</xsl:text>

	<xsl:for-each select="word">
		<xsl:call-template name="word-simp"/>
	</xsl:for-each>
	<xsl:text>}{</xsl:text>

	<xsl:for-each select="word">
		<xsl:if test="position()!=1"><xsl:text> </xsl:text></xsl:if>
		<xsl:call-template name="word-pinyin"/>
	</xsl:for-each>
	<xsl:text>}{</xsl:text>

	<xsl:apply-templates select="idiomatic"/>
	<xsl:text>}
</xsl:text>
</xsl:template>

<xsl:template match="expansion_word">
	<xsl:text>\expword{</xsl:text>
	<xsl:value-of select="normalize-space(.)"/>
	<xsl:text>}
</xsl:text>
</xsl:template>

<xsl:template match="key_vocabulary | supplementary_vocabulary">
	<xsl:for-each select="word">
		<xsl:text>\dictitem{</xsl:text>
		<xsl:apply-templates select=".//traditional"/>
		<xsl:text>}{</xsl:text>
		<xsl:apply-templates select=".//simplified"/>
		<xsl:text>}{</xsl:text>
		<xsl:apply-templates select=".//latex-pinyin"/>
		<xsl:text>}{</xsl:text>
		<xsl:apply-templates select=".//literal"/>
		<xsl:text>}
</xsl:text>
	</xsl:for-each>
</xsl:template>

<xsl:template match="/">
<xsl:text>
\documentclass[12pt]{article}
\usepackage{CJKutf8}
\usepackage{fullpage}
\usepackage{multicol}
\usepackage{pinyin}

\newcommand{\lessontitle}[1]{\section*{#1}}

\newcommand{\lessonid}[1]{\texttt{http://www.chinesepod.com/lessons/#1}}

\newenvironment{keyvocab}{\subsection*{Key Vocabulary}
	\begin{multicols}{3} \begin{description}}
	{\end{description} \end{multicols}}
\newenvironment{suppvocab}{\subsection*{Supplementary Vocabulary}
	\begin{multicols}{3} \begin{description}}
	{\end{description} \end{multicols}}

\newenvironment{diagsent}{\subsection*{Dialogue Sentences}
	\begin{itemize}}{\end{itemize}}
\newenvironment{expsent}{\subsection*{Expansion Sentences}
	\begin{itemize}}{\end{itemize}}

% parameters: trad, simp, pinyin, def
\newcommand{\dictitem}[4]{\item[\LARGE #1] \CJKfamily{gkai} #2 \CJKfamily{bsmi} \\
        \emph{#3} \\
        #4}

% parameters: speaker, trad, simp, pinyin, idiomatic
\newcommand{\diagitem}[5]{\item[\textbf{#1:}] \CJKfamily{bkai} #2 \CJKfamily{gbsn} \\
	#3 \\
	#4 \\
	\emph{#5} \\ }

\newcommand{\expitem}[4]{\item \CJKfamily{bkai} #1 \CJKfamily{gbsn} \\
	#2 \\
	#3 \\
	\emph{#4} \\ }

\newcommand{\expword}[1]{\subsubsection*{\CJKfamily{gbsn} #1}}

\begin{document}

\begin{CJK}{UTF8}{bsmi}

{\center \Huge \bf We Love Chinesepod}
</xsl:text>

	<xsl:for-each select="lesson">
		<xsl:text>\lessontitle{</xsl:text>
			<xsl:apply-templates select="title_and_level"/>
			<xsl:text>}
</xsl:text>

		<xsl:text>\lessonid{</xsl:text>
			 <xsl:apply-templates select="lesson_id"/>
			<xsl:text>}
</xsl:text>

		<xsl:for-each select="key_vocabulary">
			<xsl:text>\begin{keyvocab}
</xsl:text>
			<xsl:apply-templates select="."/>
			<xsl:text>\end{keyvocab}
</xsl:text>
		</xsl:for-each>

		<xsl:for-each select="supplementary_vocabulary">
			<xsl:text>\begin{suppvocab}
</xsl:text>
			<xsl:apply-templates select="."/>
			<xsl:text>\end{suppvocab}
</xsl:text>
		</xsl:for-each>

		<xsl:for-each select="dialogue_sentences">
			<xsl:text>\begin{diagsent}
</xsl:text>
			<xsl:for-each select="sentence">
				<xsl:call-template name="diagitem"/>
			</xsl:for-each>

			<xsl:text>\end{diagsent}
</xsl:text>
		</xsl:for-each>

		<xsl:for-each select="expansion_sentences">
			<xsl:text>\begin{expsent}
</xsl:text>
			<xsl:apply-templates select="sentence|expansion_word"/>
			<xsl:text>\end{expsent}
</xsl:text>
		</xsl:for-each>
	</xsl:for-each>
	<xsl:text>\end{CJK}
\end{document}
</xsl:text>
</xsl:template>

</xsl:stylesheet>

