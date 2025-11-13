> urls_to_redownload.txt

for missing_file in missing_SB_*.txt; do
    obs_dir=$(basename "$missing_file" | sed 's/missing_SB_//; s/\.txt$//')
    echo "Processing $obs_dir"

    while read -r sbnum; do
        echo "Looking for SB $sbnum in $obs_dir"
        # Redirect grep output both to the file and the console for debugging
        grep -h "${obs_dir}" html*.txt | grep "SB${sbnum}" | tee -a urls_to_redownload.txt
    done < "$missing_file"
done
