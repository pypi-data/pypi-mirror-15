# genomicassertions

[![Build Status](https://travis-ci.org/dakl/genomicassertions.svg?branch=master)](https://travis-ci.org/dakl/genomicassertions)
[![Coverage Status](https://coveralls.io/repos/github/dakl/genomicassertions/badge.svg?branch=master)](https://coveralls.io/github/dakl/genomicassertions?branch=master)
[![PyPI version](https://badge.fury.io/py/genomicassertions.svg)](https://badge.fury.io/py/genomicassertions)

`genomicassertions` is a python package which adds methods to test commonly generated files in the genomics field.

# Installation

`pip install genomicassertions`

# Examples

Use the `VariantAssertions` or `ReadAssertions` mixin in your test class to get access to the methods.

## VCF files

For VCF files, the following methods exist:

* `assertVcfHasVariantAt(vcf, chrom, pos)`
* `assertVcfHasSample(vcf, sample)`
* `assertVcfHasVariantWithChromPosRefAlt(vcf, chrom, pos, ref, alt)`
* `assertVcfHasVariantWithChromPosId(vcf, chrom, pos, variant_id)`
* `assertVcfHasVariantWithCall(vcf, chrom, pos, sample, call)`

## BAM files

* `assertBamHasCoverageAt(self, bam, coverage, chrom, pos)`
* `assertBamHasHeaderElement(self, bam, header_element)`
* `assertBamHeaderElementEquals(self, bam, header_element_name, header_element_value)`

### Examples

#### VCF files
~~~python
from genomicassertions.variantassertions import VariantAssertions

class TestVariants(unittest.TestCase, VariantAssertions):
    vcf = "tests/variants.vcf.gz"
    vcf_with_genotypes = "tests/variants-with-genotypes.vcf.gz"

    def test_variant_at(self):
        self.assertVcfHasVariantAt(self.vcf, 3, 178936091)

    def test_variant_with_chrom_pos_ref_alt(self):
        self.assertVcfHasVariantWithChromPosRefAlt(self.vcf_with_genotypes, 1, 3062915, 'G', 'C')
        self.assertVcfHasVariantWithChromPosRefAlt(self.vcf_with_genotypes, 1, 3062915, 'G', 'T')

    def test_variant_with_id(self):
        self.assertVcfHasVariantWithChromPosId(self.vcf_with_genotypes, 1, 3062915, 'id3D')

~~~

`assertVcfHasVariantWithCall()` asserts that individual items in a sample call are set. The parameter `call` is a dict with the items to test. The dict does not have to be complete, i.e. not all fields in the call have to be tested.

~~~python    
    def test_vcf_has_variant_with_call(self):
        self.assertVcfHasVariantWithCall(self.vcf_with_genotypes, 1, 3184885, 'B',
                                         call={'GT': '1/2', 'DP': 10})
~~~

#### BAM files

~~~python
from genomicassertions.readassertions import ReadAssertions

class TestReads(unittest.TestCase, ReadAssertions):
    bam = "tests/3_178936091.bam"

    # assert coverage as chrom:pos
    def test_has_coverage_as_pos(self):
        self.assertBamHasCoverageAt(self.bam, coverage=324, chrom=3, pos=178936091)

    def test_bam_has_header_element(self):
        self.assertBamHasHeaderElement(self.bam, header_element="HD")

    def test_header_element_equals(self):
        self.assertBamHeaderElementEquals(self.bam,
                                          header_element_name='HD',
                                          header_element_value={'SO': 'coordinate',
                                                                'VN': '1.3'}
                                          )
~~~


# File requirements

`genomicassertions` requires the vcf files to be compressed with `bgzip` and indexed with `tabix` in order to work. This is required for the random access to variants provided by the index, which gives a significant performance increase over using non-indexed vcf files. Bam files have to be indexed.
