fd . sources scripts js style | entr -rs './scripts/make_site.sh; python -m http.server -d site'
