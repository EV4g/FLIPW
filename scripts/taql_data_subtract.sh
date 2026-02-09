for ms in $(cat big-mslist.txt); do
    echo "Processing $ms..."
    taql "UPDATE $ms SET CORRECTED_DATA = DATA - MODEL_DATA"
done