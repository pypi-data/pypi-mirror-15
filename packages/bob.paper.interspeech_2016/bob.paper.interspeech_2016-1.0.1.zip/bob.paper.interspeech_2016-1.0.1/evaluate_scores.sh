
#feature names and pretty titles for them
features=(gmm_scfc20_onlydeltas)
prettytitles=("SCFC(20) $\Delta\Delta^2$, GMM512" )


# types of experiments
postfixes=(avspoof_phys)
prettypostfixes=(", AVspoof-PA")

indxfixes=0
for p in "${postfixes[@]}"; do
  indxfeat=0
  for f in "${features[@]}"; do
    echo "=============================================================="
    echo "Evaluate scores for '${f}' features of ${database} database"
    echo "=============================================================="

    scorepath_dev="./scores/${p}/${f}_20/scores-"
    scorepath="./scores/${p}/${f}_20/scores-"

    plotnames+=("${p}_${f}")
    command="-n 10 -m 60 -t ${scorepath_dev}dev-attack -d ${scorepath_dev}dev-real -f ${scorepath}eval-attack -e ${scorepath}eval-real -o plots_${p}_${f}_20"

    echo $command --pretty-title "${prettytitles[indxfeat]}${prettypostfixes[indxfixes]}"
    bin/plot_pad_results.py  $command --pretty-title "${prettytitles[indxfeat]}${prettypostfixes[indxfixes]}"

    # if need to plot for each attack
#    bin/plot_pad_results.py $command -s replay
#    bin/plot_pad_results.py $command -s all -k all --pretty-title "${prettytitles[indxfeat]}${prettypostfixes[indxfixes]}"
#    bin/plot_pad_results.py $command -s replay -k laptop --pretty-title "${prettytitles[indxfeat]}${prettypostfixes[indxfixes]}"
#    bin/plot_pad_results.py $command -s replay -k laptop_HQ_speaker --pretty-title "${prettytitles[indxfeat]}${prettypostfixes[indxfixes]}"
#    bin/plot_pad_results.py $command -s replay -k phone1 --pretty-title "${prettytitles[indxfeat]}${prettypostfixes[indxfixes]}"
#    bin/plot_pad_results.py $command -s replay -k phone2 --pretty-title "${prettytitles[indxfeat]}${prettypostfixes[indxfixes]}"
#    bin/plot_pad_results.py $command -s voice_conversion -k physical_access --pretty-title "${prettytitles[indxfeat]}${prettypostfixes[indxfixes]}"
#    bin/plot_pad_results.py $command -s speech_synthesis -k physical_access --pretty-title "${prettytitles[indxfeat]}${prettypostfixes[indxfixes]}"
#    bin/plot_pad_results.py $command -s voice_conversion -k physical_access_HQ_speaker --pretty-title "${prettytitles[indxfeat]}${prettypostfixes[indxfixes]}"
#    bin/plot_pad_results.py $command -s speech_synthesis -k physical_access_HQ_speaker --pretty-title "${prettytitles[indxfeat]}${prettypostfixes[indxfixes]}"
#    bin/plot_pad_results.py $command -s voice_conversion -k logical_access --pretty-title "${prettytitles[indxfeat]}${prettypostfixes[indxfixes]}"
#    bin/plot_pad_results.py $command -s speech_synthesis -k logical_access --pretty-title "${prettytitles[indxfeat]}${prettypostfixes[indxfixes]}"
    indxfeat=$(( indxfeat + 1 ))
  done
  indxfixes=$(( indxfixes + 1 ))
done
echo bin/plot_far_frr_pad.py -t ${plotnames[@]} -p 20 -d plots -o stats.txt
bin/plot_far_frr_pad.py -t ${plotnames[@]} -p 20 -d plots -o stats.txt
