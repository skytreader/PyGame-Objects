for f in *py
do
    expand -t 4 $f > temp
    cat temp > $f
    echo "Expanded $f"
done

rm temp

