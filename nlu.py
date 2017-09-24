import sys
import os
import json
sys.path.append(os.path.join(os.getcwd(),'..'))
import watson_developer_cloud
import watson_developer_cloud.natural_language_understanding.features.v1 as features

nlu = watson_developer_cloud.NaturalLanguageUnderstandingV1(version='2017-02-27',
                                                            username='1aad1810-2bb7-435b-b33d-ea0afccb0c37',
                                                            password='rbzX0VcHx07r')
print(dir(features))
response = nlu.analyze(text='what is number of open tickets ?',
            features=[features.Relations(), features.Keywords()])

print(json.dumps(response, indent=2))
