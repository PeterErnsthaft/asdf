for FILE in $(ls save_*)
do
  ./sed_magic.sh "${FILE}"
done

