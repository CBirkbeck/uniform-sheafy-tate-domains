<?xml version="1.0" encoding="UTF-8"?>
<!-- Default PreTeXt LaTeX conversion + paperforge custom-element handling.
     paper-init rewrites the placeholder from paper.toml [build]. -->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:import href="core-local/latex.xsl"/>
  <xsl:variable name="author-metadata"
                select="document('../content/authors.xml', /)/author-metadata"/>
  <!-- PDF metadata lists every author (title/subject come from core) -->
  <xsl:param name="latex.preamble.late">
    <xsl:text>\hypersetup{pdfauthor={</xsl:text>
    <xsl:for-each select="/pretext/article/frontmatter/titlepage/author">
      <xsl:if test="position() &gt; 1"><xsl:text> and </xsl:text></xsl:if>
      <xsl:value-of select="personname"/>
    </xsl:for-each>
    <xsl:text>}}</xsl:text>
  </xsl:param>
  <!-- formalization badges are an HTML feature; drop in print -->
  <xsl:template match="lean"/>
  <!-- prose term links are an HTML feature; keep only their text here -->
  <xsl:template match="termref"><xsl:apply-templates/></xsl:template>
  <!-- alphabetic bibliography labels (tex2ptx bib-labels option) -->
  <xsl:template match="biblio[@label]" mode="serial-number">
    <xsl:choose>
      <xsl:when test="starts-with(@label, 'bib-')">
        <xsl:value-of select="substring-after(@label, 'bib-')"/>
      </xsl:when>
      <xsl:otherwise><xsl:value-of select="@label"/></xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  <!-- \class is MathJax-only; make it a no-op wrapper in LaTeX. Generated
       tables use booktabs rules, so load the package explicitly here as in
       the classic arXiv conversion. -->
  <xsl:param name="latex.preamble.early">
    <xsl:text>\usepackage{booktabs}&#xa;</xsl:text>
    <xsl:text>\usepackage{xurl}&#xa;</xsl:text>
    <xsl:text>\providecommand{\class}[2]{#2}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{00AC}{\ensuremath{\neg}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{00B7}{\ensuremath{\cdot}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{03B9}{\ensuremath{\iota}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{03D6}{\ensuremath{\varpi}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{207A}{\ensuremath{^{+}}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{2080}{\ensuremath{_{0}}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{2081}{\ensuremath{_{1}}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{2082}{\ensuremath{_{2}}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{2083}{\ensuremath{_{3}}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{2115}{\ensuremath{\mathbb{N}}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{211D}{\ensuremath{\mathbb{R}}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{2192}{\ensuremath{\to}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{2194}{\ensuremath{\leftrightarrow}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{21A5}{\ensuremath{\uparrow}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{2200}{\ensuremath{\forall}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{2203}{\ensuremath{\exists}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{2208}{\ensuremath{\in}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{2227}{\ensuremath{\wedge}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{2264}{\ensuremath{\leq}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{2286}{\ensuremath{\subseteq}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{22C3}{\ensuremath{\bigcup}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{27E8}{\ensuremath{\langle}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{27E9}{\ensuremath{\rangle}}&#xa;</xsl:text>
    <xsl:text>\DeclareUnicodeCharacter{1D4AA}{\ensuremath{\mathcal O}}</xsl:text>
  </xsl:param>

  <!-- Author-status footnotes (content/authors.xml author-footnote records):
       the marker belongs to the affiliation that carries it, so the note is
       emitted after \maketitle rather than through \thanks, which would add
       a second marker beside the author's name. -->
  <xsl:template name="author-status-footnotes">
    <xsl:for-each select="$author-metadata/record[author-footnote]">
      <xsl:text>\begingroup&#xa;</xsl:text>
      <xsl:text>\renewcommand{\thefootnote}{\fnsymbol{footnote}}&#xa;</xsl:text>
      <xsl:text>\footnotetext[</xsl:text>
      <xsl:value-of select="position()"/>
      <xsl:text>]{</xsl:text>
      <xsl:apply-templates select="author-footnote/node()"/>
      <xsl:text>}&#xa;</xsl:text>
      <xsl:text>\endgroup&#xa;</xsl:text>
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="article/frontmatter/titlepage">
    <xsl:text>\maketitle&#xa;</xsl:text>
    <xsl:call-template name="author-status-footnotes"/>
    <xsl:text>\thispagestyle{empty}&#xa;</xsl:text>
  </xsl:template>
</xsl:stylesheet>
