# Kota Miura (miura@cmci.info)
# Spatial k-means clustering
# 20150325

from ij import IJ
from org.apache.commons.math3.ml.clustering import Clusterable, KMeansPlusPlusClusterer
from java.util import ArrayList
from jarray import array
from ij import Macro
from ij.gui import GenericDialog;


# extract coordinates of white (255) pixels from stack
# @return Python List of Lists (3D coordinate)
# @TODO better be scaled in Z
def parsePoints(imp):
	pntsA = []
	for k in range(imp.getStackSize()):
		ip = imp.getStack().getProcessor(k+1)
		for j in range(ip.getHeight()):
			for i in range(ip.getWidth()):
				if ip.getPixel(i, j) == 255:
					#IJ.log(str(i) + ', ' + str(j) + ', ' + str(k)+ ': ' + str(ip.getPixel(i, j)))
					pntsA.append([i, j, k])
	return pntsA

# A class implementing Clusterable interface in Appache Commons Math
# see http://commons.apache.org/proper/commons-math/apidocs/index.html?org/apache/commons/math3/ml/clustering/Clusterer.html
class PosWrap(Clusterable):
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		self.pa = array([x, y, z], 'd')
		
	def getPoint(self):
		return self.pa
# The main function
def core(imp):
	pntsA = parsePoints(imp)
	# Points must be passed to the Clusterer in Java List of Clusterable. 
	pntsAL = ArrayList()
	for apnt in pntsA:
		pntsAL.add(PosWrap(apnt[0], apnt[1], apnt[2]))
	
	awrap = pntsAL.get(0)
	pp = awrap.getPoint()
	#print pp
	
	clusterer = KMeansPlusPlusClusterer(Number_of_Cluster, Iteration)
	res = clusterer.cluster(pntsAL)
	outimp = imp.duplicate()
	for i in range(res.size()):
		if Verbose:
			IJ.log('Cluster: ' + str(i))
		for apnt in res.get(i).getPoints():
			xpos = apnt.getPoint()[0]
			ypos = apnt.getPoint()[1]
			zpos = apnt.getPoint()[2]
			if Verbose:
				IJ.log('... ' + str(xpos) + ', ' + str(ypos) + ', ' + str(zpos))
			outimp.getStack().getProcessor(int(zpos)+1).putPixel(int(xpos), int(ypos), i+1)
	return outimp
	
Verbose = False
if IJ.isMacro():
    opt = getArgument()# ImageJ specific function Macro.getOptions()
    if len(opt) == 0:
        opt = OPT_PLACEHOLDER
    IJ.log(opt)
    optA = opt.split()
    Number_of_Cluster = int(optA[0])
    Iteration = int(optA[1])
else:
   gd =  GenericDialog("KMean Points Clustering", IJ.getInstance())
   gd.addNumericField("Expected Number of Clusters", 4, 0)
   gd.addNumericField("Iterations", 10, 0)
   gd.showDialog()
   Number_of_Cluster = int(gd.getNextNumber())
   Iteration = int(gd.getNextNumber())
imp = IJ.getImage()
outimp = core(imp)
outimp.show()
IJ.run(outimp, "glasbey inverted", "")
		



	
