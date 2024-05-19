Australian Hydrological Geospatial Fabric (Geofabric) PRODUCT SUITE
National V3.3
--------------------------------------------------------------------------
The Geofabric National version 3.3.x product suite comprises 6 products:

 - Geofabric Surface Network                  (SH_Network)
 - Geofabric Surface Cartography	      (SH_Cartogarphy)
 - Geofabric Surface Catchments		      (SH_Catchments)
 - Geofabric Hydrology Reporting Catchments   (HR_Catchments)
 - Geofabric Hydrology Reporting Regions      (HR_Regions)
 - Geofabric Groundwater Cartography	      (GW_Cartograpy)

Please note:
Version 3.x products are currently supported by a product Guide and product 
overview relationships diagram. Further Version 3.x documentation is under 
development.

Version 3.x products have kept the same structure (schema) as V2.x products, 
with the exception of two additional feature classes and additional feature 
class attribution. Therefore V2.x documentation can be utilised, taking into 
consideration the use of higher resolution foundation input data in Version 3.x.
Also within existing Version 2.x documentation, references to V2.1, dates, scales,
product identifiers, geographic extent, etc cannot be relied upon when viewed 
for Version 3.x purposes.

Documentation is available at
http://www.bom.gov.au/water/geofabric/documentation.shtml.

Geofabric Sample Toolset
The Geofabric Sample Toolset can be used with Version 3.x data, but a D8 raster 
dataset is not currently supplied for each drainage division, which means 
the Create Catchments tool cannot be utilised with the spilt (2) option.
A D8 raster can be arranged on request. 
A topology file for use in the toolset is also not currently provided, 
but can be created by the user, utilising the Geofabric Sample Toolset.
A National V3.3 Topology file is currently being created, but takes over a week to complete,
so we strongly encourage users to only create smaller topology files for your specific
areas of interest.
#Note Create Catchments with the split option is not supported by ESRI in ArcMap10.6.0

The Latest Geofabric Sample Toolset can be downloaded from
ftp://ftp.bom.gov.au/anon/home/geofabric/

REQUIREMENTS
------------
Data is supplied in zipped files, with each zip file containing:
 - 1 ESRI File Geodatabase (a folder containing a collection of files)
 - 1 ESRI layer file (2 for SH_Cartography)
 - 1 README.TXT file
 - 2 metadata files (HTML & XML)

 These are compatible with ESRI ArcGIS Desktop 10.3 and above.


INSTALLATION
------------
Unzip the downloaded file, making sure to maintain the internal directory
structure.
The resulting File Geodatabase (directory) should end with .gdb.

For example, when unzipped correctly and viewed in Windows File Explorer,
the contents of the downloaded file
SH_Network_GDB_V3_3.zip should be:

 - 1 folder called SH_Network_GDB (which contains the following files):
 - 1 ESRI File Geodatabase (folder) called SH_Network.gdb
 - 1 ESRI Layer file called Geofabric Surface Network - National V3.3.lyr
 - 1 README file called Geofabric National_V3_3_PRODUCT_README.txt
 - 1 metadata HTM file called SH_Network_GDB_National_V3_3.html
 - 1 metadata XML file called SH_Network_GDB_National_V3_3.xml 

The File Geodatabase and layer file are then available to be used in
ArcGIS Desktop, version 10.3 and above.


METADATA 
--------
- Product level metadata is available in both XML and HTML formats within each
zip file.
- File GeoDataBase (FGDB), Feature Dataset and Feature Class metadata can be viewed in
ArcCatalog using the ISO 19139 stylesheet.


USER FEEDBACK
-------------
Your feedback is vital to assist us in maintaining a business case to support
and enhance Geofabric products. Also, by letting us know how you are using, or
want to use the Geofabric; you will enable us to better serve user needs.

If you have any questions or feedback (including questions of a more technical 
nature) on V3.x products, please feel to contact us via the AHGF mailbox and 
we'll endeavour to respond to your query in a timely manner. 

More Generally if you have any ideas, issues or questions related to any 
Geofabric product and its potential use, we'd be delighted to hear from you, 
again preferable through our email AHGF@bom.gov.au.


LICENSING
---------
We request attribution as © Commonwealth of Australia (Bureau of Meteorology) 2022
https://creativecommons.org/licenses/by/4.0/


CONTACT INFORMATION
-------------------
Water Information - Environmental Prediction Services
Community Services Group
Bureau of Meteorology
GPO Box 2334 CANBERRA ACT 2601
Web: http://www.bom.gov.au/water/geofabric/
Email: ahgf@bom.gov.au


KNOWN ISSUES
----------------------------------------

#GF-488	The NCBPfafstetter table is not populated for this release. The
 	table doesn't contain any data relating to Pfafstetter coding. There are no
	plans to create pfafstetter coding in V3, with the table to be reviewed and
	potentially deprecated. Remaining attribution and any new V3.x attribution 
	derived from ANUDEMCatchment Toolkit outputs will be either included in 
	AHGFCatchments or new tables. 

#GF-571 AHGFWaterbody DEMH Attribution is mostly Null, therefore doesn't correctly 
	reflect	which Waterbodies were enforced / not enforced into the DEM for V3.x. 
	In V2.x all waterbodies were enforced into the DEM. This DEMH attribution will
	be reviewed if there is a business rational to do so.

#GF-575 AHGFCatchment [ExtSegLink] attribution is not available for the Lake Eyre Basin 
	Drainage Division. Alternate analyse will be required to attribute internally 
	draining basins (Sinks) that have terminating stream segments, which have the 
	potential to contribute overland flows to the main drainage network which flows
	into Lake Eyre.

#GF-596 Nearly all AHGFWaterbody features have a value for NetNodeID, regardless of 
	whether they have been enforced into the DEM. This includes those that don't 
	intersect AHGFNetworkStream features. Also identified that AHGFWaterbody 
	features that weren't enforced into the DEM but have intersecting streams, 
	have alternate associated NetNodeId's to the features that they intersect with.
	Further review and documentation is required.

#GF-597 In AHGFContractedCatchment there are inconsistent groupings of sink noflow 
	catchments for GhostNode outlet (Gauge) Contracted Catchments in 6 Drainage 
	Divisions, these being the Murray Darling Basin, Pilbara-Gascoyne, South West 
	Coast, South West Plateau, North West Plateau and Tanami-Timor Sea Coast.
	Typically, most noticeable in low relief areas (floodplains) where a Contracted 
	Ghost Node (Gauge) is splitting a long stream reach. These Contracted Catchments
	will be progressively reviewed and updated as part of Geofabric maintenance work
	around important Gauging station catchments, along with further analysis of 
	ANUDEMCatchment Toolkit outputs to support automated improvements.

#GF-598 AHGFContractedCatchment attribution [ConCatID] is incorrect for select 
	AHGFCatchments upstream of GhostNode outlet (Gauge) Contracted Catchments. The 
	AHGFCatchment that overlaps the GhostNode can only have one ConCatID attributed 
	to it, which is generally the downstream ConCatID. But AHGFCatchments further 
	upstream until the next Contracted Node are incorrectly attributed with the 
	downstream ConCatID, instead of the ConCatID of the AHGFContractedCatchment they 
	reside in. These will be reviewed and updated in future releases as required.

#GF-599 AHGFContractedCatchment's include a small number of marginally (~30m) disjointed 
	Contracted Catchments around Contracted Node junctions. These junctions have two 
	inflow (contributing) Contracted Catchments, but associated sinks (that if filled 
	would flow to the junction) have been grouped to the incorrect inflow Contracted 
	Catchment. These will be reviewed and updated in future releases as required.

#GF-600 SH_Cartography AHGFMappedStreams and AHGFMappedNodes do not include any [FromNode],
	[ToNode], [NextdownID], [UpstreamGeodesicLength] or [ContractedNodeID] attribution,
	nor any associated records in 3 tables; AHGFMappedNodeConnectivityUp, 
	AHGFMappedNodeConnectivityDown and AHGFMappedStream_FS. AHGFMappedStreams and 
	Nodes are still components of the SH_Cartography_Net geometric network which can
	be traced in ArcMap using the Utility Network Analysts tools. Also, HR_Catchments 
	AHGFNode [MapNodeId] values are all Null. There are no plans to update this 
	attribution, with empty tables to be reviewed and potentially deprecated. 
	AHGFMappedStreams can still be related to AHGFNetworkStreams through [AusHydroID].

#GF-604 SH_Network Gauging Station AHGFNetworkNode features have 30 records with NULL
	[ConNodeID]. These 30 NULL records should be updated in a future release.

#GF-605 SH_Network AHGFNetworkStream & SH_Cartography AHGFMapped Stream have problematic
	flow directions on the anabranching tributaries on the lower reaches of the 
	Fitzroy River (QLD).

#GF-606 HR_Catchments AHGFLink within the Tanami -Timor Sea Coast Darianage Division, 
	has 2 records without FConNodeID and TConNoeID attribution.

#GF-607 SH_Cartography AHGFSea, AHGFEstuary and AHGFTerrainBreakline contain
	no features, and there are no current plans to populate these feature classes in V3.x.

#GF-608 HR_Catchment features within the Cooper Creek RiverRegion in the Lake Eyre Drainage
	Division didn't receive any expert input to re-include important Contracted Node 
	Features (Gauges & V2.x Contracted Nodes) into this simplified node link catchment
	network. Important Contracted Node features will be reviewed for re-inclusion 
	as required based on stakeholder input and updated in future releases.
	Was incorrectly labelled as known issue GF-601 in V3.2.1 release notes

#GF-609 HR_Catchment AHGFContractedCatchment boundaries may be inconsistent with the boundaries
        of the new V3.3 HR_Region StationCatchments feature class. Differences are primarily 
	around the outlets of StationCatchments/AHGFContractedNodes, with 
	AHGFContractedCatchments still to be updated. HR_Catchments ContractedCatchment 
	boundaries will be progressively updated to be consistent with StaionCatchments where
	logical to do so. There may be instances where StationCatchments are different based 
	on expert review taking into consideration man changes to the drainage network.
	In these instances the expert review undertaken will be documented in StationCatchments.
	Many inconsistencies are related to sinkbasins as documented under #GF-597

CHANGELOG
---------
= KEY ===================
    # Breaks back-compat
    ! Feature
    - Bugfix
      + Sub-comment
    . Internal change
==========================


    Changes at National V3.3
    -----------------
     ! Includes additional V3.x Groundwater product with 5 feature classes
	- GW_Cartography
	    - AHGFAquiferBoundary
	    - AHGFAquiferContour
	    - AHGFAquiferOutcrop
	    - AHGFAquiferSalinity
	    - AHGFAquiferYield
		

     ! Includes 1 additional feature class in HR_Regions product
	- StationCatchments which represent upstream contributing 
	  catchments of important Gauging Stations

    - Further select review undertaken of AHGFNetworkNode's that represent
      important Gauging Stations, particulalry GhostNodes to improve
      locations on AGHFNetworkStream's. Done in parallel with creation of 
      new StationCatchments feature class.

    - Further select review undertaken of AHGFWaterbody NetNodeID's for 
      water storages, to ensure the most logiocal node is attributed as 
      the outlet of the storage.
      


    Changes at National V3.2.1
    -----------------

    ! This Readme file updated in all product download zip files.                                               

    - (GF-601) HR_Regions - the two feature dataset relationships have
      been renamed, names had been incorrectly swapped, but each 
      relationship still worked correctly.

    - (GF-602) SH_Network AHGFNetworkNodeLUT Domains set for 
      [Confidence] and [GN_QA_Code]. No attribution has been updated.



    Changes at National V3.2
    -----------------

    ! Includes 3 additional V3.x products
	- SH_Cartography
	- SH_Catchments
	- HR_Catchments

    - Further review undertaken of AHGFNetworkNode Ghost Nodes that 
      represent important Gauging Stations, to improve locations on 
      AGHFNetworkStream's, and remove duplicates that represent the 
      same monitoring location of surface water features.

    ! HR_Catchments product includes ~2700 AHGFContractedNode features
      that represent Important Gauging Stations, along with associated 
      upstream reach AHGFContractedCatchment and AHGFLink features.

    ! HR_Regions product includes 1 additional RiverRegion feature in 
      the Lake Eyre Draiange Divisn, named 'Bullo River-Lake Bancannia',
      which was split off from previously named feature 
      'Cooper Creek - Bullo River' with remaining split feature part 
      renamed to 'Cooper Creek'.  

    ! SH_Network product includes 2 additional relationships between
      AHGFNetworkStream and AHGFCatchment. These relationships include 
      additional internally draining basins (Sinks) which if filled have 
      the potential to contribute overland flows to AHGFNetworkStreams.
      These two relationship are SNLCatchmentDrainstoSegment using 
      AHGFCatchment [SegNolink] attribution and ESLCatchmentDrainstoSegment
      which uses AHGFCatchment [ExtSegLink], the latter includes inland 
      terminating AHGFNetworkStream catchments and their associated sinks,
      related to an AHGFNetworkstream segment that is part of a drainage
      network with a coastal terminating outlet node.

    - (GF-572) SH_Network Product now includes:
	      	- Table 	AHGFNetworkConnectivityDown
	      	- Table 	AHGFNetworkConnectivityDown
	      	- Table 	AHGFNetworkStreamFS
	      	- Relationship  NetNodeDrainsWaterbody
     	      	- Relationship  NetNodeDrainsCatchment

    - (GF-573) HR_Regions Product now includes:
	      	- Feature Class RiverRegion
	     	- Table 	AWRADDContractedCatchmentLookup
	       	- Table 	RRContractedCatchmentLookup
	       	- Relationship 	DrainDivMapsToConCatchment
	       	- Relationship 	RiverRegMapstoConCatchment

    - (GF-574) AHGFCatchment attribute fields NetNodeID and NextDownID 
	       is populated in this release. NetNodeID is required
	       for the relationship NetNodeDrainsCatchment.

    - (GF-577) AHGFWaterbody attribute field NetNodeID is populated in 
	       this release. NetNodeID is required for the relationship 
	       NetNodeDrainsWaterbody.



    Changes at National V3.0.5 Beta
    -----------------

    All products
    ------------
    ! All Metadata has been reviewed and updated to reflect Version 3.0.5 Beta updates.


    SH_Network
    ----------
    ! 4 previously publicly released V3.x Drainage Divisions have been updated, details below:
	! SEV V3.1.1 & TAS V3.0
		! additional Monitoring Point Network Nodes (MPNN), and small amount of MPNN QA.
		# No AHGFGhostNode feature class, all features now included in AHGFNetworkNode 
		  as was done in V2.1.1. 
		  Previous AHGFGhostNode attribution is available in the Table AHGFNetworkNode_LUT,
		  with a supporting Layer file 'AHGFNetwork node - Gauging Stations'.

	# PG & NWP, reprocessed with slightly different Catchment boundaries, and additional MPNN's. 

	
    <No prior change logs, with this being the first National extent V3.x Geofabric product to be released.>
	-------------------------------------------------------------------------------