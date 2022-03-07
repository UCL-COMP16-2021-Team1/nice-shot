from analysis_pipeline import analyse_video

# essentially what will be used in django - since there's only one function we may want to just directly put it in django but I'm leaving this here for the sake of making the code extendable
def analyse(capture):
    analyse_video(capture)