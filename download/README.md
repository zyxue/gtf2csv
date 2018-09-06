### URLs:

* http://ftp.ensembl.org/pub/release-75/gtf/homo_sapiens/Homo_sapiens.GRCh37.75.gtf.gz
* ftp://ftp.ensembl.org/pub/grch37/update/gtf/homo_sapiens/Homo_sapiens.GRCh37.87.gtf.gz
* ftp://ftp.ensembl.org/pub/release-92/gtf/homo_sapiens/Homo_sapiens.GRCh38.92.gtf.gz
* ftp://ftp.ensembl.org/pub/release-93/gtf/homo_sapiens/Homo_sapiens.GRCh38.93.gtf.gz
* ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_28/gencode.v28.annotation.gtf.gz

### index gtf

reference: http://www.htslib.org/doc/tabix.html

```
for gtf in $(find . -name '*.gtf.gz'); do
    gtf_prefix=$(dirname ${gtf})/$(basename ${gtf} .gz)
    echo gtf_prefix: ${gtf_prefix}
    unpigz -c ${gtf_prefix}.gz | \grep -v ^"#" | sort -k1,1 -k4,4n | bgzip > ${gtf_prefix}.sorted.gz
    tabix ${gtf_prefix}.sorted.gz
done
```
