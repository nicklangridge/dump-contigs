#!/usr/bin/env python

import requests, sys, json, urllib

REST_BASE = 'http://rest.ensembl.org/'

def main():
  if len(sys.argv) < 2:
    sys.exit('Usage: {} <species>'.format(sys.argv[0]))
  else:
    dump_species_contigs(sys.argv[1])
  return

def dump_species_contigs(species):
  method = 'info/assembly/{}'.format(species)
  assembly_info = rest(method)
  coord_sys = assembly_info['default_coord_system_version']
  chrs = assembly_info['karyotype']
  #print bed_header(species, coord_sys)
  for chr in chrs:
    dump_chr_contigs(species, coord_sys, chr)
  return

def dump_chr_contigs(species, coord_sys, chr):
  method = 'map/{}/{}/{}'.format(species, coord_sys, chr)
  response = rest(method, {'target_coord_system' : 'contig'})
  for mapping in response['mappings']:
    start = mapping['original']['start']
    end = mapping['original']['end']
    score = 0
    name = mapping['mapped']['seq_region_name']
    strand = '+' if (mapping['original']['strand'] == 1) else '-'
    print bed_line([chr, start, end, name, score, strand])
  return

def bed_header(species, coord_sys):
  return 'track name="Contigs" description="{} {} Contigs"'.format(species, coord_sys)

def bed_line(data):
  return '\t'.join(map(str, data))

def rest(method, args = {}):
  url = REST_BASE + method + '/?' + urllib.urlencode(args)
  response = requests.get(url, headers={ 'Content-Type' : 'application/json'})
  if not response.ok:
    response.raise_for_status()
    sys.exit()
  return response.json()

main()


