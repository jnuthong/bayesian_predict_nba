# -*- encoding: utf-8 -*-
import re
import sys
import codecs
import thinkbayes
import datetime
import numpy as np

class NBA(thinkbayes.Suite):
	"""
	"""

	def __init__(self, mu, sigma, name=''):
		"""
		"""

		pmf = thinkbayes.MakeGaussianPmf(mu, sigma, 1)
		thinkbayes.Suite.__init__(self, pmf, name=name)

	def Likelihood(self, data, hypo):
		"""
		"""
		lam = hypo
		k = data 
		like = thinkbayes.EvalPoissonPmf(k, lam)
		return like

	def updateSet(self, dataset):
		"""
		"""
		for data in dataset:
			for hypo in self.Values():
				like = self.Likelihood(data, hypo)
				self.Mult(hypo, like)

		return self.Normalize()

def MakeGoalPmf(suite, high=100, low=0):
    """Makes the distribution of goals scored, given distribution of lam.

    suite: distribution of goal-scoring rate
    high: upper bound

    returns: Pmf of goals per game
    """
    metapmf = thinkbayes.Pmf()

    for lam, prob in suite.Items():
				# TODO: low should not be zero in nba
        pmf = thinkbayes.MakePoissonPmf(lam, int(high), low=0)
        metapmf.Set(pmf, prob)

    mix = thinkbayes.MakeMixture(metapmf, name=suite.name)
    return mix

def main():
	"""
	"""
	info = dict()
	date = datetime.datetime.now().strftime("%Y%m%d")
	with open("/Users/baidu/Desktop/ThinkBayes/detail/%s" % date) as file_obj:
		for line in file_obj:
			line = line.strip("\n\r").split(",")
			playid, num, side, home, a, b, score, c, d = line		
			key = side + home
			info[key] = [playid, num, a, b, score, c, d]
	
	if len(sys.argv) >= 3:
			score = float(sys.argv[2])
	else:
			score = 0

	with open(sys.argv[1]) as file_obj:
			line = file_obj.readline()
			line = line.strip("\n\r").split(" ")
			size, home = line[0:2]
			total_mu, total_sigma, side_mu, side_sigma = [float(ele) for ele in line[2:]]

			line = file_obj.readline()
			line = line.strip("\n\r").split(",")
			total_data = [float(ele) for ele in line]

			line = file_obj.readline()
			line = line.strip("\n\r").split(",")
			side_data = [float(ele) for ele in line]
			# line = file_obj.readline()
			# score = float(line.strip("\n\r"))	

			line = file_obj.readline()
			line = line.strip("\n\r").split(",")
			home_data = [float(ele) for ele in line]
			home_mu = np.mean(home_data)
			home_sigma = np.std(home_data)

			side_team = NBA(mu=side_mu, sigma=side_sigma, name="side_team") 
			home_team = NBA(mu=home_mu, sigma=home_sigma, name="home_team")
			total_team = NBA(mu=total_mu, sigma=total_sigma, name="total_team")
			total_team.updateSet(home_data)
			side_team.updateSet(side_data)

			goal_side = MakeGoalPmf(side_team, low=side_mu - side_sigma * 2, high=side_mu + side_sigma * 2)
			goal_home = MakeGoalPmf(home_team, low=home_mu - home_sigma * 2, high=home_mu + home_sigma * 2)
			goal_total = MakeGoalPmf(total_team, low=total_mu - total_sigma * 2, high=total_mu + total_sigma * 2)
			# diff = goal_total - goal_side - goal_side
			diff = goal_home - goal_side
			key = size + home
			home_win = diff.ProbGreater(-1.0 * score)
			home_loss = diff.ProbLess(-1.0 * score)
			# home_win = diff.ProbGreater(0)
			# home_loss = diff.ProbLess(0)
			# p_tie = diff.Prob(0)
			value = info[key]
			print "================ Game start =================="
			print size, home, value[1], total_mu, total_sigma, side_mu, side_sigma
			print score, value[2], value[3]
			print "Home win: %.4f, expected %.4f" % (home_win, home_win * float(value[3]))
			print "Side win: %.4f, expected %.4f" % (home_loss, home_loss * float(value[2]))
			print "####### Change Score #######"
			print value[4], value[5], value[6]
			home_win = diff.ProbGreater(-1.0 * float(value[4]))
			home_loss = diff.ProbLess(-1.0 * float(value[4]))
			print "Home win: %.4f, expected %.4f" % (home_win, home_win * float(value[6]))
			print "Side win: %.4f, expected %.4f" % (home_loss, home_loss * float(value[5]))
	with open(sys.argv[1]) as file_obj:
			print "+++++++++ game detail +++++++++"
			data = file_obj.read()
			print data
			print "================ Game end =================="
	

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding("utf-8")
	main()
