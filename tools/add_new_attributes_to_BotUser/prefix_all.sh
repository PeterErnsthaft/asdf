for FILE in $(ls save_*)
do
  ./add_prefix.sh "$(cat prefix)" "${FILE}"
done

