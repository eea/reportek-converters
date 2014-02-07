<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:wfd="http://water.eionet.europa.eu/schemas/dir200060ec">

<!-- Stylesheet created by Hermann Peifer, EEA, March 2010 -->

<!-- Variable definition for tab delimited output -->
<xsl:variable name="newline" select="'&#x0A;'"/>
<xsl:variable name="tab" select="'&#x09;'"/>

<xsl:output method="text" encoding="UTF-8"/>

<xsl:template match="/">

	<!-- Ugly hack, but we want a generic stylesheet and I don't get xsltproc -param to work  -->
	<xsl:apply-templates select="/wfd:ProtectedAreas/wfd:ProtectedArea/wfd:EUProtectedAreaCode"/>
	<xsl:apply-templates select="/wfd:SurfaceWaterBodies/wfd:SurfaceWaterBody/wfd:EUSurfaceWaterBodyCode"/>
	<xsl:apply-templates select="/wfd:GroundWaterBodies/wfd:GroundWaterBody/wfd:EUGroundWaterBodyCode"/>
	<xsl:apply-templates select="/wfd:RBDSUCA/wfd:RiverBasinDistrict/wfd:EURBDCode"/>
	<xsl:apply-templates select="/wfd:RBDSUCA/wfd:RiverBasinDistrict/wfd:SubUnits/wfd:SubUnit/wfd:EUSubUnitCode"/>

</xsl:template>

<xsl:template match="wfd:EUProtectedAreaCode|wfd:EUSurfaceWaterBodyCode|wfd:EUGroundWaterBodyCode|wfd:EURBDCode|wfd:EUSubUnitCode">
	<xsl:value-of select="local-name()"/>	<xsl:value-of select="$tab"/>
	<xsl:value-of select="."/>		<xsl:value-of select="$newline"/>
</xsl:template>

</xsl:stylesheet>
