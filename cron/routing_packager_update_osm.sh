#!/usr/bin/env bash

usage()
{
    echo "usage: routing_packager_update_osm.sh --interval -i [minutely|hourly|*daily*|weekly] --dir-pbf -d /app/data/osm"
}

interval=daily
pbf_dir=/app/data/osm

# Get the arguments
while [ "$1" != "" ]; do
    case $1 in
        -i | --interval )       shift
                                interval=$1
                                ;;
        -d | --dir-pbf )        shift
                                pbf_dir=$1
                                ;;
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

# Validate at least the interval
if ! [[ "$interval" =~ ^(minutely|hourly|daily|weekly)$ ]]; then
  echo "argument --interval '${interval}' is not a valid option."
  usage
  exit 1
fi

opts=""
if [[ $interval == 'hourly' ]]; then
  opts+='--hour --day'
elif [[ $interval =~ ^(daily|weekly)$ ]]; then
  opts+='--day'
fi

pbf_expansion="${pbf_dir}/*.pbf"
pbf_count=$(ls $pbf_expansion | wc -l)
counter=0
for f in $pbf_expansion
do
  fn=$(basename "${f}")
  pbf_name_updated="updated_${fn}"
  pbf_updated="${pbf_dir}/${pbf_name_updated}"

  # Extract the bbox with osmium
  bbox=$(osmium fileinfo -j ${f} | jq .header.boxes[0])
  # Sanitize the bbox string
  bbox_sanitized=${bbox//[$'\t\r\n ']}

  # Only keep the temp files if it's not the last PBF
  (( counter++ ))
  if [[ $counter != "${pbf_count}" ]]; then
    osmupdate -v --keep-tempfiles ${opts} -b="${bbox_sanitized:1:-1}" "${f}" "${pbf_updated}" || exit 1
  else
    osmupdate -v ${opts} -b="${bbox_sanitized:1:-1}" "${f}" "${pbf_updated}" || exit 1
    rm -r osmupdate_temp || true
  fi

  # finally overwrite the previous file
  mv "${pbf_updated}" "${f}"
done