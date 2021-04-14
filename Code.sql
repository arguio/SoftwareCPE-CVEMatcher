UPDATE SoftwareCPE
SET CPE = REPLACE(CPE, CHAR(13), '')

SELECT SoftwareCPE.ProductOriginal, SoftwareCPE.CPE, CVE.cpe23uri, CVE.ID, CVE.Description
FROM SoftwareCPE
INNER JOIN CVE ON SoftwareCPE.CPE = CVE.cpe23uri
WHERE SoftwareCPE.ProductOriginal LIKE '%sublime%'
  AND SoftwareCPE.ProductOriginal LIKE '%text%'
  AND SoftwareCPE.ProductOriginal LIKE '%3%'


UPDATE CVE
SET CVE.V2ImpactScore=(TRY_PARSE( CVE.V2ImpactScore AS NUMERIC(4,2) USING 'El-GR' )),
CVE.V3ImpactScore=(TRY_PARSE( CVE.V3ImpactScore AS NUMERIC(4,2) USING 'El-GR' )),
CVE.V3ExploitabilityScore=(TRY_PARSE( CVE.V3ExploitabilityScore AS NUMERIC(4,2) USING 'El-GR' )),
CVE.V3BaseScore=(TRY_PARSE( CVE.V3BaseScore AS NUMERIC(4,2) USING 'El-GR' )),
CVE.V2ExploitabilityScore=(TRY_PARSE( CVE.V2ExploitabilityScore AS NUMERIC(4,2) USING 'El-GR' )),
CVE.V2BaseScore=(TRY_PARSE( CVE.V2BaseScore AS NUMERIC(4,2) USING 'El-GR' ))
