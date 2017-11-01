import sys  
import params
import os.path
from ECBParser import *
from ECBHelper import *
from HDDCRPParser import *
from StanParser import *
from CCNN import *
from get_coref_metrics import *

# parses the corpus and runs Coref Resoultion on the mentions
class CorefEngine:
	if __name__ == "__main__":

		# handles passed-in args
		args = params.setCorefEngineParams()

		# stan = StanParser(args) # loads stanford's parsed output

		hddcrp_parsed = HDDCRPParser(args.hddcrpFile) # loads HDDCRP's pred or gold mentions file
		print("# H-UIDs in",str(args.hddcrpFile),":", str(len(hddcrp_parsed.MUIDToHMentions.keys())))

		corpus = ECBParser(args)
		helper = ECBHelper(corpus, args)

		#helper.addStanfordAnnotations(stan)
		#exit(1)

		# trains and tests the pairwise-predictions
		corefEngine = CCNN(args, corpus, helper, hddcrp_parsed)

		(pairs, predictions) = corefEngine.run()

		stoppingPoints =[0.49,0.501,0.51,0.52,0.53,0.54,0.55,0.56,0.57,0.58,0.59,0.601]

		for sp in stoppingPoints:
			predictedClusters = corefEngine.clusterHPredictions(pairs, predictions, sp)
			print("we returned # clusters:",str(len(predictedClusters.keys())))
			corefEngine.writeCoNLLFile(predictedClusters, sp)
			#print("done writing CoNLL file")
		exit(1)

		for sp in stoppingPoints:
			(predictedClusters, goldenClusters) = corefEngine.clusterPredictions(pairs, predictions, sp)
			print("RESULTS FOR STOPPING POINT: ",str(sp))
			bcub_p, bcub_r, bcub_f1, muc_p, muc_r, muc_f1, ceafe_p, ceafe_r, ceafe_f1, conllf1 = get_conll_scores(goldenClusters, predictedClusters)
			print("bcub - rec:",str(bcub_r))
			print("bcub - prec:",str(bcub_p))
			print("bcub - f1:",str(bcub_f1))
			print("muc - rec:",str(muc_r))
			print("muc - prec:",str(muc_p))
			print("muc - f1:",str(muc_f1))
			print("ceafe - rec:",str(ceafe_r))
			print("ceafe - prec:",str(ceafe_p))
			print("ceafe - f1:",str(ceafe_f1))
			print("conll - f1:",str(conllf1))
		'''
		hddcrp_gold = HDDCRPParser(goldHDDCRPFile)
		print("# H-UIDs golds:", str(len(hddcrp_gold.UIDToHMentions.keys())))

		hddcrp_pred = HDDCRPParser(predHDDCRPFile)
		print("# H-UIDs preds:", str(len(hddcrp_pred.UIDToHMentions.keys())))
		hddcrp = hddcrp_gold

		numInGold = 0
		numMissingFromPred = 0
		numInPred = 0
		numMissingFromGold = 0
		for uid in hddcrp_gold.UIDToHMentions.keys():
			if uid not in hddcrp_pred.UIDToHMentions.keys():
				numMissingFromPred += 1
			numInGold += 1
		for uid in hddcrp_pred.UIDToHMentions.keys():
			if uid not in hddcrp_gold.UIDToHMentions.keys():
				numMissingFromGold += 1
			numInPred += 1

		print("numInGold",numInGold)
		print("numMissingFromPred",numMissingFromPred)
		print("numInPred",numInPred)
		print("numMissingFromGold",numMissingFromGold)
		'''
		# parses corpus

		'''
		numRefs = 0
		numDMs = 0
		for d in helper.testingDirs:
			numRefs += len(corpus.dirToREFs[d])
			for doc_id in corpus.dirToDocs[d]:
				numDMs += len(corpus.docToDMs[doc_id])
		print("numRefs",numRefs)
		print("numDMs:",numDMs)

		print("# ECB-UIDs:", str(len(corpus.UIDToMentions.keys())))
		
		docsMissingFromH = set()
		numEMentions = 0
		numEMentionsMissing = 0
		numDMentions = 0
		numDMentionsMissing = 0
		for doc_id in corpus.docToDMs.keys():
			#print("ecbdoc:", str(doc_id)," has ",str(len(corpus.docToDMs[doc_id])), "mentions")
			if doc_id in hddcrp.docToHMentions.keys():
				for dm in corpus.docToDMs[doc_id]:
					mention = corpus.dmToMention[dm]
					if mention.UID not in hddcrp.UIDToHMentions.keys():
						print("\t* hddcrp doesn't have:", str(mention.UID))
						numEMentionsMissing += 1
					numEMentions += 1
			else:
				docsMissingFromH.add(doc_id)

		for doc_id in hddcrp.docToHMentions.keys():
			if doc_id in corpus.docToDMs.keys():
				for mention in hddcrp.docToHMentions[doc_id]:
					if mention.UID not in corpus.UIDToMentions.keys():
						print("* corpus doesn't have:", str(mention.UID))
						numDMentionsMissing += 1
					numDMentions += 1
			else:
				print("ERROR: ecb is missing", str(doc_id))

		print("numEMentions:",numEMentions)
		print("numEMentionsMissing:",numEMentionsMissing)
		print("numDMentions:",numDMentions)
		print("numDMentionsMissing:",numDMentionsMissing)
		print("docsMissingFromH:", str(len(docsMissingFromH)))
			#	print("\thddcrp has the doc w/", str(len(hddcrp.docToHMentions[doc_id])), "mentions")
		exit(1)
		'''





