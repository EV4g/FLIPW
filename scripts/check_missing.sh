for dir in L*; do
    echo "Checking directory: $dir"
    
    ls "$dir"/*SB???_*.MS 2>/dev/null | \
    sed -nE 's/.*SB([0-9]{3}).*/\1/p' | sort > existing.txt
    
    seq -w 0 242 > expected.txt
    
    missing=$(comm -23 expected.txt existing.txt)
    
    if [ -n "$missing" ]; then
        echo "Missing SB files in $dir: $missing"
        echo "$missing" > missing_SB_${dir}.txt
    else
        echo "No missing SB files in $dir"
    fi
done
