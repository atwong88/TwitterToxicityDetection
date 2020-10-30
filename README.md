# Toxic/Abusive Comments Detection

Project By: Martin Ambrozic, Matthew Canute, Adriena Wong

Social media has always been a convenient and useful way to share content and ideas online, but interactions between users can often become toxic, with harassment, abusive comments, and hate speech. This may make it difficult for some users to express their opinions freely or may detract conversations. The goal of this project was the common task of building a toxicity classifier, but with the additional goal of determining whether having the context of the Twitter community surrounding each Tweet would have any meaningful impact on the model results. However, we did not find any meaningful difference between the Twitter communities we collected, and this paper will also investigate some of the reasons as to why we think this may be the case. We also investigated other measurable language differences between communities.

In 2018, Kaggle released a toxicity classification competition on a dataset containing comments from Wikipedia’s talk page. We have used this dataset for model training, although the nature of Wikipedia comments seemed to differ slightly from the tweets we were trying to classify.

# Project Structure
- /data : contains datasets used for training and testing as well as the saved model files.
- /data_collection : contains the scripts used to collect Twitter data from its streaming API
- /main_project : containing the main project analysis notebook, requirements.txt, and the script used for training
- /notebooks : contains work-in-progress notebooks used for experimentation and analysis
- /output : contains the predictions from our model as well as a simple evaluation script
- /topic_modelling : contains topic_modelling jupyter notebook and pickled model and dictionary files

# Final Report

[report.pdf](https://github.com/atwong88/Twitter_Toxicity_Detection/files/5466925/report.pdf)
