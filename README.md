# DNAInfo Neighborhood Mapping Analysis

DNAInfo recently asked Chicagoans to draw what they thought were the boundaries
of their neighborhood: [This is Where Chicagoans Say The Borders of Their Neighborhoods Are](https://www.dnainfo.com/chicago/20150928/loop/this-is-where-chicagoans-say-borders-of-their-neighborhoods-are)

Currently the Python script pulls the TopoJSON and GeoJSON from DNAInfo's site,
to make it possible to analyze which neighborhoods have the most responses, as well
as which neighborhoods have the most and least agreement on their boundaries, and
what the characteristics of their neighborhood are.

All drawn neighborhood polygons are combined in `dna_neighborhoods.geojson`, with
the `neighborhood` property listing each polygon's respective neighborhood.

### Requirements

Must have `wget` installed. If you're using a Mac, you can use Homebrew to install
it with `brew install wget`.

All information comes from [DNAInfo Chicago](https://www.dnainfo.com/chicago/)
