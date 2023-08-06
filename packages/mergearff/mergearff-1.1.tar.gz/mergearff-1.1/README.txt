####mergearff


####Use Case

When you want to merge two arff files with Weka, it gives you 2 options as merging and appending. Appending uses for merging two arff files which have exactly same headers. And merging option uses for merging attributes for same instances. But sometimes we need append arff files and their headers. So imagine you have 2 arff files which have same attributes(but different headers) and different instances. 

	1.arff, 30 instances
	----------------------------------
	@relation 1.arff
	..
	@attribute weather {rainy, sunny}
	..

	2.arff, 40 instances
	----------------------------------
	..
	@attribute weather {cloudly}
	..


	merged.arff, 70 instances
	---------------------------------
	..
	@attribute weather {rainy, sunny, cloudly]
	..


####Usage
    $ mergearff [1.arff] [2.arff] [merged.arff]

####Installation
	$ [sudo] pip install mergearff