######################################################################################################
######################################################################################################
# function hfssNewProject(fid)
#
# Description :
# -------------
# This function creates the necessary VBScript to create a new HFSS project
# file, set it as the active project.
#
# Parameters:
# -----------
# fid         - file identifier of the VBScript File.
# -------------------------------------------------------------------------- #
def hfssNewProject(fid):

# Preamble.
	fid.write('Dim oHfssApp\n');
	fid.write('Dim oDesktop\n');
	fid.write('Dim oProject\n');
	fid.write('Dim oDesign\n');
	fid.write('Dim oEditor\n');
	fid.write('Dim oModule\n');
	fid.write('\n');

# Create a New Project.
	fid.write('Set oHfssApp  = CreateObject("AnsoftHfss.HfssScriptInterface")\n');
	fid.write('Set oDesktop = oHfssApp.GetAppDesktop()\n');
	fid.write('oDesktop.RestoreWindow\n');
	fid.write('oDesktop.NewProject\n');

# The new project created is the active project.
	fid.write('Set oProject = oDesktop.GetActiveProject\n');


# ----------------------------------------------------------------------------
# function hfssInsertDesign(fid, designName, [designType = 'driven modal'])
# 
# Description :
# -------------
# Create the necessary VB Script to insert an HFSS Design into the Project 
# and set it as the active design.
#
# Parameters :
# ------------
# fid        - file identifier of the HFSS script file.
# designName - name of the new design to be inserted.
# designType - (Optional String) choose from the following:
#              1. 'driven modal' (default)
#			   2. 'driven terminal'
#			   3. 'eigenmode'
# 
# Note :
# ------
# This function is usually called after a call to either hfssNewProject()
# or hfssOpenProject(), but this is not necessary.
#
# Example :
# ---------
# fid = fopen('myantenna.vbs', 'wt')
# ...
# hfssInsertDesign(fid, 'Dipole_SingleElement')
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
def hfssInsertDesign(fid, designName,designType = 'driven modal'):



# create the necessary script.
	fid.write('\n')
	fid.write('oProject.InsertDesign "HFSS", ')
	fid.write('"%s", '%designName)
	deType = designType.lower()
	if deType=='driven terminal':
		fid.write('"DrivenTerminal", ""\n')
	elif deType== 'driven modal':
		fid.write('"DrivenModal", ""\n')
	else:
		fid.write('"Eigenmode", ""\n')
	fid.write('Set oDesign = oProject.SetActiveDesign("%s")\n'%designName)
	fid.write('Set oEditor = oDesign.SetActiveEditor("3D Modeler")\n')

'''% ----------------------------------------------------------------------------
% function hfssBox(fid, Name, Start, Size, Units, [Center1], [Radius1], ...
%                  [Axis1], [Center2], [Radius2], [Axis2], ...)
% 
% Description :
% -------------
% Create the VB Script necessary to create a Box (or Cuboid) in HFSS. This 
% function also provides for optional holes (specified by their Center, 
% Radii and Axes) in the box. This feature is useful to allow things like
% vias, cables etc., to penetrate the box without intersection violations.
%
% Parameters :
% ------------
% fid     - file identifier of the HFSS script file.
% Name    - name of the box (appears in HFSS).
% Start   - starting location of the box (specify as [x, y, z]).
% Size    - size of the box (specify as [sx, sy, sz]).
% Units   - units of the box (specify using either 'in', 'mm', 'meter' or 
%           anything else defined in HFSS).
% Center  - (Optional) center of the hole to be punched through the box.
%           It can lie anywhere within or on the surface of the box.
% Radius  - (Optional) radius of the hole to be punched through the box.
% Axis    - (Optional) axis of the hole to be punched through the box.
% 
% Note :
% ------
% If you happen to specify a hole that lies outside the box, it will have
% no effect. The script will run without interruption. 
%
% Example :
% ---------
% fid = fopen('myantenna.vbs', 'wt');
% ... 
% % a Box with 2 holes punched thro' it.
% hfssBox(fid, 'FR4_Base', [-bpHeight/2, -baseLength/2, 0], [bpHeight, ...
%         baseLength, -baseThick], 'in', [cX1, cY1, cZ1], R1, 'Z',...
%         [cX2, cY2, cZ2], R2, 'X');
%
% ----------------------------------------------------------------------------'''
#import os
#############################################################################
############################## non check ####################################
#----------------------------------------------------------------------------
#function hfssInsertSolution(fid, Name, fGHz, [maxDeltaS = 0.02], 
#                            [maxPass = 25])
#
#Description :
#-------------
#Creates the VBScript necessary to insert a Solution Setup in HFSS. 
#
#Parameters :
#------------
#fid       - file identifier of the HFSS script file.
#Name      - name of the solution setup.
#fGHz      - solution frequency (in GHz).
#maxError  - maximum error that can be tolerated (should be between 0 and 1,
#            default is 0.02).
#maxPasses - max # of passes to be run before the simulation is declared
#            as 'did not converge' (default is 25).
#
#Note :
#------
#
#Example :
#---------
#fid = fopen('myantenna.vbs', 'wt');
#... 
#hfssInsertSolution(fid, 'Setup750MHz', 0.75, 0.01, 100);
#----------------------------------------------------------------------------
def hfssInsertSolution(fid, Name, fGHz, *args):

#arguments processor.

	if (len(args) < 1):
		maxDeltaS = 0.02;
		maxPass = 25;
	elif (len(args) < 2):
		maxDeltaS = args[0];
		maxPass = 25;
	else:
		maxDeltaS = args[0];
		maxPass = args[1];

	#create the necessary script.
	fid.write('\n');
	fid.write('Set oModule = oDesign.GetModule("AnalysisSetup")\n');
	fid.write('oModule.InsertSetup "HfssDriven", _\n');
	fid.write('Array("NAME:%s", _\n'% Name);
	fid.write('"Frequency:=", "%fGHz", _\n'% fGHz);
	fid.write('"PortsOnly:=", false, _\n');
	fid.write('"maxDeltaS:=", %f, _\n'% maxDeltaS);
	fid.write('"UseMatrixConv:=", false, _\n');
	fid.write('"MaximumPasses:=", %d, _\n'% maxPass);
	fid.write('"MinimumPasses:=", 1, _\n');
	fid.write('"MinimumConvergedPasses:=", 1, _\n');
	fid.write('"PercentRefinement:=", 20, _\n');
	fid.write('"ReducedSolutionBasis:=", false, _\n');
	fid.write('"DoLambdaRefine:=", true, _\n');
	fid.write('"DoMaterialLambda:=", true, _\n');
	fid.write('"Target:=", 0.3333, _\n');
	fid.write('"PortAccuracy:=", 2, _\n');
	fid.write('"SetPortMinMaxTri:=", false)\n');
#############################################################################
##########################  non check #######################################
#----------------------------------------------------------------------------
#function hfssInterpolatingSweep(fid, Name, SolutionName, fStartGHz, ...
#                               fStopGHz, [nPoints = 1000], [nMaxSols = 101], 
#                               [iTol = 0.5])
#
#Description :
#-------------
#Create the VB Script necessary to add an interpolating sweep to an existing
#solution.
#
#Parameters :
#------------
#fid          - file identifier of the HFSS script file.
#Name         - name of the interpolating sweep. 
#SolutionName - name of the solution to which this interpolating sweep needs
#               to be added.
#fStartGHz    - starting frequency of sweep in GHz.
#fStopGHz     - stop frequency of sweep in GHz.
#nPoints      - # of output points (defaults to 1000).
#nMaxSols     - max # of interpolating points that need to be solved (more 
#               points will guarentee convergence) - defaults to 101.
#iTol         - interpolation tolerance (defaults to 0.5).
#
#Note :
#------
#
#Example :
#---------
#fid = fopen('myantenna.vbs', 'wt');
#... 
#hfssInterpolatingSweep(fid, 'Interp600to900MHz', 'Solve750MHz', 0.6, ...
#                       0.9, 1000, 101, 0.5);
#
#----------------------------------------------------------------------------

##############################################################################
########################   non check ########################################
#----------------------------------------------------------------------------
#function hfssSolveSetup(fid, SetupName)
#
#Description :
#-------------
#Creates the VB script to solve a given solution setup.
#
#Parameters :
#------------
#fid       - file identifier of the HFSS script file.
#SetupName - name of the setup to be solved.
#
#Note :
#------
#
#Example :
#---------
#fid = fopen('myantenna.vbs', 'wt');
#... 
#hfssSolveSetup(fid, 'Setup750MHz');
#----------------------------------------------------------------------------

def hfssSolveSetup(fid, SetupName):

	fid.write('\n');
	fid.write('oDesign.Solve _\n');
	fid.write('    Array("%s") \n'% SetupName);

#########################33

def hfssInterpolatingSweep(fid, Name, SolutionName, fStartGHz,fStopGHz, *args):

	#arguments processor.
	if (len(args) < 1):
		nPoints = 1000;
		nMaxSols = 101;
		iTol = 0.5;
	elif (len(args) < 2):
		nPoints = args[0];
		nMaxSols = 101;
		iTol = 0.5;
	elif (nargin < 3):
		nPoints = args[0];
		nMaxSols = args[1];
		iTol = 0.5;
	else:
		nPoints = args[0];
		nMaxSols = args[1];
		iTol = args[2];


	#create script.
	fid.write('\n');
	fid.write('Set oModule = oDesign.GetModule("AnalysisSetup")\n');

	fid.write('oModule.InsertDrivenSweep _\n');
	fid.write('"%s", _\n'% SolutionName);
	fid.write('Array("NAME:%s", _\n'% Name);
	fid.write('"Type:=", "Interpolating", _\n');
	fid.write('"InterpTolerance:=", %f, _\n'% iTol);
	fid.write('"InterpMaxSolns:=", %d, _\n'% nMaxSols);
	fid.write('"SetupType:=", "LinearCount", _\n');
	fid.write('"StartFreq:=", "%fGHz", _\n'% fStartGHz);
	fid.write('"StopFreq:=", "%fGHz", _\n'% fStopGHz);
	fid.write('"Count:=", %d, _\n'% nPoints);
	fid.write('"SaveFields:=", false, _\n');
	fid.write('"ExtrapToDC:=", false)\n');

#######################################

def hfssBox(fid, Name, Start, Size, Units, *args):
	fid.write('\n')
	fid.write('oEditor.CreateBox _\n')
	# Box parameters.
	fid.write('Array("NAME:BoxParameters", _\n')
	fid.write('"XPosition:=", "%f%s", _\n' % (Start[0], Units))
	fid.write('"YPosition:=", "%f%s", _\n' % (Start[1], Units))
	fid.write('"ZPosition:=", "%f%s", _\n' % (Start[2], Units))
	fid.write('"XSize:=", "%f%s", _\n'% (Size[0], Units))
	fid.write('"YSize:=", "%f%s", _\n' % (Size[1], Units))
	fid.write('"ZSize:=", "%f%s"), _\n'% (Size[2], Units))

	#Box Attributes.
	fid.write('Array("NAME:Attributes", _\n')
	fid.write('"Name:=", "%s", _\n' % (Name))
	fid.write('"Flags:=", "", _\n')
	fid.write('"Color:=", "(132 132 193)", _\n')
	fid.write('"Transparency:=", 0.75, _\n')
	fid.write('"PartCoordinateSystem:=", "Global", _\n')
	fid.write('"MaterialName:=", "vacuum", _\n')
	fid.write('"SolveInside:=", true)\n')

	# Add Holes.
	nHoles = len(args)/3
	#print(nHoles)
	#os.system('pause')

	# For each Hole Request create cylinder that satisfies the request and then
	# subtract it from the Box.
	for iH in range(int(nHoles)):
		print(args)
		#os.system('pause')
		Center = args[3*iH]
		Radius = args[3*iH + 1]
		Axis = args[3*iH+2].upper()

		if (Axis == 'X'):
			Center[0] = Start[0]
			Length = Size[0]
		if (Axis=='Y'):
			Center[1] = Start[1]
			Length = Size[1]
		if (Axis == 'Z'):
			Center[2] = Start[2]
			Length = Size[2]
		hfssCylinder(fid,Name+'_subhole'+ str(iH+1),Axis,Center,Radius,Length,Units)
		hfssSubtract(fid,Name,Name+'_subhole'+str(iH+1))
'''% ----------------------------------------------------------------------------
% function hfssCylinder(fid, Name, Axis, Center, Radius, Height, Units)
% 
% Description :
% -------------
% Creates the VB script necessary to model a cylinder in HFSS.
%
% Parameters :
% ------------
% fid     - file identifier of the HFSS script file.
% Name    - name of the cylinder (in HFSS).
% Center  - center of the cylinder (specify as [x, y, z]). This is also the 
%           starting point of the cylinder.
% Axis    - axis of the cylinder (specify as 'X', 'Y', or 'Z').
% Radius  - radius of the cylinder (scalar).
% Height  - height of the cylidner (from the point specified by Center).
% Units   - specify as 'in', 'mm', 'meter' or anything else defined in HFSS.
% 
% Note :
% ------
%
% Example :
% ---------
% fid = fopen('myantenna.vbs', 'wt');
% ... 
% hfssCylinder(fid, 'Cyl1', 'Z', [0, 0, 0], 0.1, 10, 'in');
% ----------------------------------------------------------------------------'''
def hfssCylinder(fid, Name, Axis, Center, Radius, Height, Units):
	fid.write('\n')
	fid.write('oEditor.CreateCylinder _\n')
	fid.write('Array("NAME:CylinderParameters", _\n')
	fid.write('"XCenter:=", "%f%s", _\n'% (Center[0], Units))
	fid.write('"YCenter:=", "%f%s", _\n'% (Center[1], Units))
	fid.write('"ZCenter:=", "%f%s", _\n'% (Center[2], Units))
	fid.write('"Radius:=", "%f%s", _\n'% (Radius, Units))
	fid.write('"Height:=", "%f%s", _\n'% (Height, Units))
	fid.write('"WhichAxis:=", "%s"), _\n'% (Axis.upper()))

	# Cylinder Properties.
	fid.write('Array("NAME:Attributes", _\n')
	fid.write('"Name:=", "%s", _\n'% (Name))
	fid.write('"Flags:=", "", _\n')
	fid.write('"Color:=", "(132 132 193)", _\n')
	fid.write('"Transparency:=", 0, _\n')
	fid.write('"PartCoordinateSystem:=", "Global", _\n')
	fid.write('"MaterialName:=", "vacuum", _\n')
	fid.write('"SolveInside:=", true)\n')
	fid.write('\n')
'''% ----------------------------------------------------------------------------
% hfssSubtract(fid, blankParts, toolParts)
%
% Description:
% ------------
% Creates the necessary VB script to subtract a set of tool parts from a set 
% of blank parts, a.k.a., will produce blank parts - tool parts.
%
% Parameters :
% ------------
% fid        - file identifier of the HFSS script file.
% blankParts - a cell array of strings that contain the blank parts.
% toolParts  - a cell array of strings that contain the tool parts.
%
% Example :
% ---------
% fid = fopen('myantenna.vbs', 'wt');
% ... 
% hfssSubtract(fid, {'BigPlate'}, {'SmallPlate'});
%
% ----------------------------------------------------------------------------'''
def hfssSubtract(fid, blankParts, toolParts):
	# Preamble.

	fid.write('\n')
	fid.write('oEditor.Subtract _\n')
	fid.write('Array("NAME:Selections", _\n')

	#Add the Blank Parts.
	fid.write('"Blank Parts:=", _\n')
	if type(blankParts) is list:
		nBlank = len(blankParts)
		fid.write('"')
		for iB in range(nBlank-1):
			fid.write('%s'%(blankParts[iB]))
		fid.write('%s", _\n'% (blankParts[nBlank-1]))
	else:
		fid.write('"%s", _\n'% (blankParts))

	# Add the Tool Parts.
	fid.write('"Tool Parts:=", _\n')
	if type(toolParts) is list:
		nTool = len(toolParts)
		fid.write('"')
		for iB in range(nTool-1):
			fid.write('%s'%(toolParts[iB]))
		fid.write('%s"), _\n'% (toolParts[nTool-1]))
	else:
		fid.write('"%s"), _\n' % (toolParts))

	# Post - Amble.
	fid.write('Array("NAME:SubtractParameters", _\n')
	fid.write('"KeepOriginals:=", false) \n')

'''% ----------------------------------------------------------------------------
% function hfssAssignMaterial(fid, Object, Material)
% 
% Description :
% -------------
% Creates the VB Script necessary to assign a material selection to an 
% existing HFSS object.
%
% Parameters :
% ------------
% fid      - file identifier of the HFSS script file.
% Object   - name of the object to which the material is to assigned.
% Material - the material to be assigned to the Object. This is a string that
%            should either be predefined in HFSS or defined using 
%            hfssAddMaterial(...)
% 
% Note :
% ------
%
% Example :
% ---------
% fid = fopen('myantenna.vbs', 'wt');
% ... 
% hfssAssignMaterial(fid, 'FR4Mount', 'FR4epoxy'); 
% ----------------------------------------------------------------------------'''
def hfssAssignMaterial(fid, Name, Material):
	fid.write('\n')
	fid.write('oEditor.AssignMaterial _\n')
	fid.write('\tArray("NAME:Selections", _\n')
	fid.write('\t\t"Selections:=", "%s"), _\n' % (Name)) 
	fid.write('\tArray("NAME:Attributes", _\n')
	fid.write('\t\t"MaterialName:=", "%s", _\n'% (Material))
	#if the material is copper, we should set solve inside to be false and for
	#other materials (in general) is should be true.
	if (Material=='copper') or (Material =='pec'):
		fid.write('\t\t"SolveInside:=", false)\n')
	else:
		fid.write('\t\t"SolveInside:=", true)\n')

'''
% -------------------------------------------------------------------------- %
% function hfssPolyline(fid, Name, Points, Units)
% Description:
% ------------
%
% Parameters:
% -----------
% Name - Name Attribute for the PolyLine.
% Points - Points as 3-Tuples, ex: Points = [0, 0, 1; 0, 1, 0; 1, 0 1];
%          Note: size(Points) must give [nPoints, 3]
% Units - can be either:
%         'mm' - millimeter.
%         'in' - inches.
%         'mil' - mils.
%         'meter' - meter (note: don't use 'm').
%          or anything that Ansoft HFSS supports.
%
'''

def hfssPolyline1(fid, Name, Points, Units,*args):
	if (len(args) < 5):
		Closed = [];
		segmentType = [];
		Color = [];
		Transparency = [];
	elif (len(args) < 6):
		segmentType = [];
		Color = [];
		Transparency = [];
	elif (len(args) < 7):
		Color = [];
		Transparency = [];
	elif (len(args) < 8):
		Transparency = [];

	if Closed == []:
		Closed = 'true';

	if segmentType == []:
		segmentType = 'Line';

	if  Color ==[]:
		Color = [0, 0, 0];

	if  Transparency == []:
		Transparency = 0.8;


	nPoints = len(Points[:, 1]);

	# Preamble.
	fid.write('\n');
	fid.write('oEditor.CreatePolyline _\n');
	fid.write('\tArray("NAME:PolylineParameters", ');
	fid.write('"IsPolylineCovered:=", true, ');
	fid.write('"IsPolylineClosed:=", %s, _\n'% Closed);

	# Enter the Points.
	fid.write('\t\tArray("NAME:PolylinePoints", _\n');
	for iP in range(nPoints-1):
		fid.write('\t\t\tArray("NAME:PLPoint", ');
		fid.write('"X:=", "%.4f%s", '% (Points[iP, 0], Units));
		fid.write('"Y:=", "%.4f%s", '% (Points[iP, 1], Units));
		fid.write('"Z:=", "%.4f%s"), _\n'% (Points[iP, 2], Units));

	fid.write('\t\t\tArray("NAME:PLPoint", ');
	fid.write('"X:=", "%.4f%s",   '% (Points[nPoints-1, 0], Units));
	fid.write('"Y:=", "%.4f%s",   '% (Points[nPoints-1, 1], Units));
	fid.write('"Z:=", "%.4f%s")_\n'% (Points[nPoints-1, 2], Units));
	fid.write('\t\t\t), _ \n');

	# Create Segments.
	fid.write('\t\tArray("NAME:PolylineSegments", _\n');
	for iP in range(nPoints-2):
		fid.write('\t\t\tArray("NAME:PLSegment", ');
		fid.write('"SegmentType:=",  "%s", '% segmentType);
		fid.write('"StartIndex:=", %d, '% iP);
		fid.write('"NoOfPoints:=", 2), _\n');

	fid.write('\t\t\tArray("NAME:PLSegment", ');
	fid.write('"SegmentType:=",  "%s", '% segmentType);
	fid.write('"StartIndex:=", %d, '% (iP+1));
	fid.write('"NoOfPoints:=", 2) _\n');
	fid.write('\t\t\t) _\n');
	fid.write('\t\t), _\n');

	# Polyline Attributes.
	fid.write('Array("NAME:Attributes", _\n');
	fid.write('"Name:=", "%s", _\n'% Name);
	fid.write('"Flags:=", "", _\n');
	fid.write('"Color:=", "(%d %d %d)", _\n'% (Color[0], Color[1], Color[2]));
	fid.write('"Transparency:=", %f, _\n'% Transparency);
	fid.write('"PartCoordinateSystem:=", "Global", _\n');
	fid.write('"MaterialName:=", "vacuum", _\n');
	fid.write('"SolveInside:=", true)\n');


#############################################################################
########################## non check ########################################
# ----------------------------------------------------------------------------
# function hfssRectangle(fid, Name, Axis, Start, Width, Height, Units)
# 
# Description :
# -------------
# Create the VB Script necessary to construct a rectangle using the HFSS
# 3D Modeler.
#
# Parameters :
# ------------
# fid     - file identifier of the HFSS script file.
# Name    - name of the rectangle object (appears in the HFSS objects tree).
# Axis    - axis that is normal to the rectangle object.
# Start   - starting location of the rectangle (one of its corners). Specify
#           as [sx, sy, sz].
# Width   - (scalar) the width of the rectangle. If the axis is 'X' then this 
#           represents the Y-axis size of the rectangle, and so on.
# Height  - (scalar) the height of the rectangle. If the axis is 'X', then 
#           this represents the Z-axis size of the rectangle, and so on. 
# Units   - specify as 'in', 'meter', 'mm', ... or anything else defined in 
#           HFSS.
#
# Note :
# ------
# Todo: a feature to add automatic holes in the rectangle object.
#
# Example :
# ---------
# fid = fopen('myantenna.vbs', 'wt');
# ... 
# # in this example, Y-axis size is 10in and Z-axis size is 20in.
# hfssRectangle(fid, 'Rect1', 'X', [0,0,0], 10, 20, 'in');

def hfssRectangle(fid, Name, Axis, Start, Width, Height, Units):

	Transparency = 0.5;

	# Preamble.
	fid.write('\n');
	fid.write('oEditor.CreateRectangle _\n');

	# Rectangle Parameters.
	fid.write('Array("NAME:RectangleParameters", _\n');
	fid.write('"IsCovered:=", true, _\n');
	fid.write('"XStart:=", "%f%s", _\n'% (Start[0], Units));
	fid.write('"YStart:=", "%f%s", _\n'% (Start[1], Units));
	fid.write('"ZStart:=", "%f%s", _\n'% (Start[2], Units));

	fid.write('"Width:=", "%f%s", _\n'% (Width, Units));
	fid.write('"Height:=", "%f%s", _\n'% (Height, Units));

	fid.write('"WhichAxis:=", "%s"), _\n'% (Axis.upper()));

	# Rectangle Attributes.
	fid.write('Array("NAME:Attributes", _\n');
	fid.write('"Name:=", "%s", _\n'% Name);
	fid.write('"Flags:=", "", _\n');
	fid.write('"Color:=", "(132 132 193)", _\n');
	fid.write('"Transparency:=", %d, _\n'% Transparency);
	fid.write('"PartCoordinateSystem:=", "Global", _\n');
	fid.write('"MaterialName:=", "vacuum", _\n');
	fid.write('"SolveInside:=", true)\n');

#############################################################################
########################## non check #######################################
#----------------------------------------------------------------------------
#function hfssAssignPE(fid, Name, ObjectList, [infGND = false])
#
#Description :
#-------------
#This function creates the VB Script necessary to assign a PEC boundary to 
#the given object(s).
#
#Parameters :
#------------
#fid     - file identifier of the HFSS script file.
#Name    - name of the PEC boundary. This will appear under "Boundaries" 
#          in HFSS
#ObjList - a cell array of objects to which the PEC boundary condition will
#          be applied.
#infGND  - (boolean) specify as true to make the PEC represent an infinite
#          ground plane (default is false).
#
#
#Note :
#------
#
#Example :
#---------
#fid = fopen('myantenna.vbs', 'wt');
#... 
#hfssAssignPE(fid, 'GNDplane', {'AntennaGND'}, true);

def hfssAssignPE(fid, Name, ObjectList, *args):

	if (len(args) < 1):
		infGND = False;
	else:
		infGND = args[0]
	## of objects.
	nObjects = len(ObjectList);

	#create the necessary script.
	fid.write('\n');
	fid.write('Set oModule = oDesign.GetModule("BoundarySetup")\n');
	fid.write('oModule.AssignPerfectE _\n');
	fid.write('Array("NAME:%s", _\n'% Name);

	#is infinite GND ?
	if (infGND):
		fid.write('"InfGroundPlane:=", true, _\n');
	else:
		fid.write('"InfGroundPlane:=", false, _\n');

	fid.write('"Objects:=", _\n'); 
	fid.write('Array(');
	for iObj in range(nObjects):
		fid.write('"%s"'% ObjectList[iObj]);
		if (iObj != nObjects-1):
			fid.write(',');
	fid.write('))\n');

#########################################################################3
######################## non check ########################################
#----------------------------------------------------------------------------
#function hfssUnite(fid, args)
#
#Description :
#-------------
#Creates the VB Script necessary for unite a given set of objects already
#present in the HFSS 3D Modeler.
#
#Parameters :
#------------
#fid      - file identifier of the HFSS script file.
#args - names of the objects that need to be united. It can be specified
#           either as a single cell array of strings, or several individual
#           cell strings containing a single object name (see example ...)
#
#Note :
#------
#
#Example :
#---------
#fid = fopen('myantenna.vbs', 'wt');
#... 
##Method 1.
#hfssUnite(fid, {'Object1', 'Object2', Object3'});
##... or Method 2.
#hfssUnite(fid, {'Object1'}, {'Object2'}, {'Object3'});
#
#----------------------------------------------------------------------------


def hfssUnite(fid, *args):

	#Preamble.
	fid.write('\n');
	fid.write('oEditor.Unite  _\n');
	fid.write('Array("NAME:Selections", _\n');
	fid.write('"Selections:=", ');

	#If the first argument is a cell then it contains a cell of strings that must
	#be united, else each argument is a cell.
	if type(args[0]) == list:
		Objects = args[0];
	else:
		Objects = args;


	#Total # of Objects.
	nObjects = len(Objects);

	#Add the Objects.
	fid.write('"');
	for iP in range(nObjects-1):
		fid.write('%s,'% Objects[iP]);
	fid.write('%s"), _\n'% Objects[nObjects-1]);

	#Postamble.
	fid.write('Array("NAME:UniteParameters", "KeepOriginals:=", false)\n');



'''% ----------------------------------------------------------------------------
% function hfssCircle(fid, Name, Axis, Center, Radius, Units, coverLines)
% 
% Description :
% -------------
% Creates the VB Script necessary to create a circle in HFSS.
%
% Parameters :
% ------------
% fid     - file identifier of the HFSS script file.
% Name    - name of the circle object (in HFSS).
% Axis    - choose between 'X', 'Y', or 'Z' to represent the circle axis.
% Center  - center of the circle (use the [x, y, z] format).
% Radius  - radius of the circle.
% Units   - units for all the above quantities (use either 'in', 'mm', 'meter'
%           or anything else defined in HFSS).
% 
% Note :
% ------
%
% Example :
% ---------
% fid = fopen('myantenna.vbs', 'wt');
% ... 
% hfssCircle(fid, 'C_Patch', 'Z', [10, 11, 12], 13, 'mm');
% ----------------------------------------------------------------------------'''
def hfssCircle(fid, Name, Axis, Center, Radius, Units, *args):
	if len(args) == 0:
		coverLines = []
	if not coverLines:
		coverLines = True

	# Preamble.
	fid.write('oEditor.CreateCircle _\n')
	fid.write('Array("NAME:CircleParameters", _\n')

	# Parameter.
	if coverLines:
		fid.write('"IsCovered:=", true, _\n')
	else:
		fid.write('"IsCovered:=", false, _\n')

	fid.write('"XCenter:=", "%f%s", _\n'% (Center[0], Units))
	fid.write('"YCenter:=", "%f%s", _\n'% (Center[1], Units))
	fid.write('"ZCenter:=", "%f%s", _\n'% (Center[2], Units))
	fid.write('"Radius:=", "%f%s", _\n'% (Radius, Units))
	fid.write('"WhichAxis:=", "%s"), _\n'% (Axis.upper()))

	# Attribute.
	fid.write('Array("NAME:Attributes", _\n')
	fid.write('"Name:=", "%s", _\n'% (Name))
	fid.write('"Flags:=", "", _\n')
	fid.write('"Color:=", "(132 132 193)", _\n')
	fid.write('"Transparency:=", 0, _\n')
	fid.write('"PartCoordinateSystem:=", "Global", _\n')
	fid.write('"MaterialName:=", "vacuum", _\n')
	fid.write('"SolveInside:=", true)\n')

'''% ----------------------------------------------------------------------------
% function hfssHollowCylinder(fid, Name, Axis, Center, inRadius, outRadius, 
%			    Height, Units)
% 
% Description :
% -------------
% Creates VB Script necessary to generate a hollow cylinder in HFSS.
%
% Parameters :
% ------------
% fid       - file identifier of the HFSS script file.
% Name      - name of the hollow cylinder (in HFSS).
% Axis      - choose between 'X', 'Y' or 'Z' for the cylinder axis.
% Center    - center of the cylinder (express as [x, y, z]).
% inRadius  - inner radius of the cylinder.
% outRadius - outer radius of the cylinder.
% Height    - cylinder height.
% Units     - units for all the quantities (use either 'in', 'mm', 'meter' or
%             anything else that is defined in HFSS).
% 
% Note :
% ------
% This function creates an extra object that is a contatenation of the Name
% with '_sub' that gets subtracted from the outer cylinder to get the hollow
% structure.
%
% Example :
% ---------
% fid = fopen('myantenna.vbs', 'wt');
% ... 
% hfssHollowCylinder(fid, 'Dipole', 'X', [-G/2, 0, 0], 0.95*R, R, L, 'in');
% ----------------------------------------------------------------------------'''
def hfssHollowCylinder(fid, Name, Axis, Center, inRadius, outRadius, Height, Units):
	hfssCylinder(fid, Name, Axis, Center, outRadius, Height, Units)
	hfssCylinder(fid, Name + '_sub', Axis, Center, inRadius, Height, Units)
	hfssSubtract(fid, Name,Name + '_sub')

'''% -------------------------------------------------------------------------- %
% hfssCoaxialCable(fid, Names, Axis, Center, Radii, Height, Units)
%
% Description :
% -------------
% This function creates the VBScript necessary to draw a Coaxial Cable in 
% HFSS. The "Coaxial Cable" can have as many cylinders as you specify. This
% function only creates the geometric structure and does not set any material
% properties.
%
% Parameters :
% ------------
% fid - file identifier of the HFSS VBScript File.
% Name - a cell of strings that contains the names of each cylinder that is a
%        part of the co-axial cable (see example).
% Axis - axis of the Coaxial Cable (choose between 'X', 'Y' or 'Z').
% Center - Coordinates of the Center of the Coaxial Cable ([x, y, z]).
% Radii - an array of Radii of the Cylinders present in the Coaxial cable.
%         each radius corresponds to the respective name specfied in the 
%         'Name' parameter.
% Height - length of the coaxial cable.
% Units - can be either 'in' or 'mm' or 'meter' or anything defined in HFSS.
%
% Example:
% ---------
% ...
% # NOTICE THAT: NAMES and RADII argument need be sorted from small to big before them become arguments of this function.
% hfssCoaxialCable(fid, ['Cyl1_In', 'Cyl1_Er', 'Cyl1_Out'], 'Z', [0, 0, 0], 
%                  0.02, 0.03, 0.04], 10, 'in')
% ...'''
def hfssCoaxialCable(fid, Names, Axis, Center, Radii, Height, Units):
	# Sort the Radii first in Ascending order.
	# THIS PART IS NOT ENOUGH CODE 
	Radii = sorted(Radii)
	iR = []
	for i in range(len(Radii)):
		iR.append(i)
	# NAMES ARGUMENT NEED BE SORTED AFTER RADII ARGUMENT IS SORTED. 
	#Get the # of Cylinders.
	nCylinders = len(Radii)

	#First create the N-1 hollow cylinders.
	for iR in range(nCylinders,1,-1):
		hfssHollowCylinder(fid, Names[iR-1], Axis, Center, Radii[iR-2],Radii[iR-1], Height, Units)

	# Finally create the inner cylinder.
	hfssCylinder(fid, Names[0], Axis, Center, Radii[0], Height, Units)
	return fid
############################################################################
#################################### non check #############################
#----------------------------------------------------------------------------
#function hfssRename(fid, oldName, newName)
#
#Description :
#-------------
#Creates the VB Script necessary to rename a HFSS Object.
#3
#Parameters :
#------------
#fid     - file identifier of the HFSS script file.
#oldName - the object's previous name.
#newName - the object's new name.
#
#Note :
#------
#
#Example :
#---------
#fid = fopen('myantenna.vbs', 'wt');
#... 
#hfssRename(fid, 'dipole1', 'dipole_one');
#
#----------------------------------------------------------------------------

def hfssRename(fid, oldName, newName):

	fid.write('\n');
	fid.write('oEditor.ChangeProperty _\n');
	fid.write('Array("NAME:AllTabs", _\n');
	fid.write('Array("NAME:Geometry3DAttributeTab", _\n'); 
	fid.write('Array("NAME:PropServers", "%s"), _\n'% oldName);
	fid.write('Array("NAME:ChangedProps", _\n');
	fid.write('Array("NAME:Name", _\n');
	fid.write('"Value:=", "%s"))))\n'% newName);
	return fid
#############################################################################
############################### non check ###################################
#----------------------------------------------------------------------------
#function hfssAssignWavePort(fid, PortName, SheetObject, nModes, isLine, ...
#			    intStart, intEnd, Units)
#
#Description :
#-------------
#Creates the VB Script necessary to assign a waveport to a (sheet-like)
#object.
#
#Parameters :
#------------
#fid         - file identifier of the HFSS script file.
#PortName    - name of the wave port (will appear under 'Boundaries').
#SheetObject - name of the (sheet-like) object to which the wave port is
#              to be assigned.
#nModes      - # of modes.
#isLine      - a boolean array of length (nModes) that specifies whether the
#              corresponding mode has an integration line or not.
#intStart    - (nModes x 3 matrix) an array of vectors that represent the
#              starting points for the integration lines for the 
#              respective modes (see note).
#intEnd      - (nModes x 3 matrix) an array of vectors that represent the
#              ending points for the integration lines for the 
#              respective modes (note note).
#Units       - specify as either 'in', 'meter', 'mm' or anything else
#              defined in HFSS.
#
#Note :
#------
#1. if an integration line is not required for a particular mode, then the
#   corresponding entries in intStart and intEnd are ignored.
#2. mostly, we will be using a single-mode and a single integration line.
#
#Example :
#---------
#fid = fopen('myantenna.vbs', 'wt');
#... 
##single mode, no integration line specified.
#hfssAssignWavePort(fid, Name, ObjectName, 1, false, [0,0,0], ...
#                 [0,0,0], Units);
#
#----------------------------------------------------------------------------

#############################################################################
############################# non check ####################################
#----------------------------------------------------------------------------
#function hfssAssignRadiation(fid, Name, Object)
#
#Description :
#-------------
#Creates the VB Script necessary to assign the radiation boundary condition
#to a (closed) Object.
#
#Parameters :
#------------
#fid     - file identifier of the HFSS script file.
#Name    - name of the radiation boundary condition (under HFSS).
#Object  - object to which the radiation boundary conditions needs to be 
#          applied.
#
#Note :
#------
#This function cannot be used to apply radiation boundary conditions to 
#individual faces of an object.
#
#Example :
#---------
#fid = fopen('myantenna.vbs', 'wt');
#... 
#hfssAssignRadiation(fid, 'ABC', 'AirBox');
#---------------------------------------------------------------------------


def hfssAssignRadiation(fid, Name, BoxObject):

	fid.write('Set oModule = oDesign.GetModule("BoundarySetup")\n');
	fid.write('oModule.AssignRadiation _\n');
	fid.write('Array("NAME:%s", _\n'% Name);
	fid.write('"Objects:=", Array("%s"))\n'% BoxObject);

###################################33
###############################################################################
##################### non check ##############################################
#----------------------------------------------------------------------------
#function hfssSetTransparency(fid, ObjectList, Value)
#
#Description
#-----------
#Creates the VB Script necessary to set the transparency of the given set of
#objects to a given value.
#
#Parameters
#----------
#fid - file identifier of the HFSS script file.
#ObjectList - a cell-array of objects whose transparency needs to be set.
#Value - the value of the objects transparency (can be between 0 and 1).
#
#Example
#-------
#hfssSetTransparency(fid, {'AirBox'}, 0.95);
#----------------------------------------------------------------------------

def hfssSetTransparency(fid, ObjectList, Value):

	#arguments processing.

	if ((Value < 0) or (Value > 1)):
		raise ValueError('transparency must be between 0 and 1!');

	if not type(ObjectList) == list:
		raise ValueError('ObjectList must be a cell-array of objects !');	

	nObj = len(ObjectList);

	fid.write('\n');
	fid.write('oEditor.ChangeProperty _\n');
	fid.write('Array("NAME:AllTabs", _\n');
	fid.write('\tArray("NAME:Geometry3DAttributeTab", _\n');
	fid.write('\t\tArray("NAME:PropServers",');
	for iO in range(nObj-1):
		fid.write('"%s", '% ObjectList[iO]);
	fid.write('"%s"), _\n'% ObjectList[nObj-1]);
	fid.write('\t\tArray("NAME:ChangedProps", _\n');
	fid.write('\t\t\tArray("NAME:Transparent", "Value:=",  %f) _\n'% Value);
	fid.write('\t\t\t) _\n');
	fid.write('\t\t) _\n');
	fid.write('\t)\n');


def hfssAssignWavePort(fid, PortName, SheetObject, nModes, isLine,intStart, intEnd, Units):

	#Preamble.
	fid.write('\n');
	fid.write('Set oModule = oDesign.GetModule("BoundarySetup") \n');
	fid.write('\n');
	fid.write('oModule.AssignWavePort _\n');
	fid.write('Array( _\n');
	fid.write('"NAME:%s", _\n'% PortName);
	fid.write('"NumModes:=", %d, _\n'% nModes); 
	fid.write('"PolarizeEField:=",  false, _\n');
	fid.write('"DoDeembed:=", false, _\n');
	fid.write('"DoRenorm:=", false, _\n');

	#Add the Mode-Lines One By One.
	for iM in range(nModes):
		fid.write('Array("NAME:Modes", _\n');
		if (isLine[iM]):
			fid.write('Array("NAME:Mode1", _\n');
			fid.write('"ModeNum:=",  %d, _\n'% iM);
			fid.write('"UseIntLine:=", true, _\n');
			fid.write('Array("NAME:IntLine", _\n');
			fid.write('"Start:=", _\n');
			fid.write('Array("%f%s", "%f%s", "%f%s"), _\n'%(intStart[0], Units, intStart[1], Units,intStart[2], Units)); 
			fid.write('"End:=", _\n');
			fid.write('Array("%f%s", "%f%s", "%f%s") _\n'%(intEnd[0], Units, intEnd[1], Units,intEnd[2], Units));
			fid.write('), _\n');
			fid.write('"CharImp:=", "Zpi")');
		else:
			fid.write('Array("NAME:Mode1", _\n');
			fid.write('"ModeNum:=",  %d, _\n'% iM);
			fid.write('"UseIntLine:=", false) _\n');
		if (iM != nModes):
			fid.write(', _\n');
	fid.write('), _\n');
	fid.write('"Objects:=", Array("%s")) \n'% SheetObject);
                            
############################################################################
############################### non check ##################################
#---------------------------------------------------------------------------
#function hfssAssignLumpedPort(fid, Name, ObjName, iLStart, iLEnd, Units, 
#                              [Resistance = 50.0], [Reactance = 0.0])
#
#Description :
#-------------
#Create the necessary VB Script to assign a Lumped Port to a given Object.
#
#Parameters :
#------------
#fid     - file identifier of the HFSS script file.
#Name    - name of the lumped port (appears under 'Boundaries' in HFSS).
#ObjName - name of the (sheet-like) object to which the lumped port is to 
#          be assigned.
#iLStart - (vector) starting point of the integration line. Specify as
#          [x, y, z].
#iLEnd   - (vector) ending point of the integration line. Specify as
#          [x, y, z].
#Units   - specify as 'meter', 'in', 'cm' (defined in HFSS).
#[Resistance] - (scalar, optional) the port resistance (defaults to 
#               50.0 Ohms)
#[Reactance]  - (scalar, optional) the port reactance (defaults to 
#               0.0 Ohms)
#
#Note :
#------
#Integration Lines are mandatory in lumped ports.
#
#Example :
#---------
#fid = fopen('myantenna.vbs', 'wt');
#... 
# hfssAssignLumpedPort(fid, 'LumpedPort', 'GapSource', [-gapL/2, 0, 0], ...
#	                 [gapL/2, 0, 0], 'meter', 75, 0);
#
#----------------------------------------------------------------------------

def hfssAssignLumpedPort(fid, Name, ObjName, iLStart, iLEnd, Units,*args):

	#arguments processor.

	if (len(args) < 1):
		Resistance = 50.0;
		Reactance = 0.0;
	elif (len(args) < 2):
		Resistance = args[0];
		Reactance = 0.0;
	else:
		Resistance = args[0];
		Reactance = args[1];

	#The usual fprintf stuff.
	fid.write('\n');
	fid.write('Set oModule = oDesign.GetModule("BoundarySetup")\n');

	fid.write('oModule.AssignLumpedPort _\n');
	fid.write('Array("NAME:%s", _\n'% Name);
	fid.write('      Array("NAME:Modes", _\n');
	fid.write('             Array("NAME:Mode1", _\n');
	fid.write('                   "ModeNum:=", 1, _\n');
	fid.write('                   "UseIntLine:=", true, _\n');
	fid.write('                   Array("NAME:IntLine", _\n');
	fid.write('                          "Start:=", Array("%f%s", "%f%s", "%f%s"), _\n'%(iLStart[0], Units, iLStart[1], Units, iLStart[2], Units));
	fid.write('                          "End:=",   Array("%f%s", "%f%s", "%f%s") _\n'% (iLEnd[0], Units, iLEnd[1], Units, iLEnd[2], Units));
	fid.write('                         ), _\n');
	fid.write('                   "CharImp:=", "Zpi" _\n');
	fid.write('                   ) _\n');
	fid.write('            ), _\n');
	fid.write('      "Resistance:=", "%fOhm", _\n'% Resistance);
	fid.write('      "Reactance:=", "%fOhm", _\n'%Reactance);
	fid.write('      "Objects:=", Array("%s") _\n'% ObjName);
	fid.write('      )\n');

# ----------------------------------------------------------------------------
# function hfssCreateReport1(fid, ReportName, Type, Display, Solution,/
#                           Sweep, Context, Domain, VarObj, DataObj):
# 
# Description :
# -------------
# Creates a new report with a single trace and adds it to the Results
# branch in the project tree.
#
# Parameters :
# ------------
# fid        - file identifier of the HFSS script file.:
# ReportName - name of the report.
# Type       - type of the report (integer 1-6). Possible values are:
#                1: "Modal S Parameters"
#                2: "Terminal S Parameters"
#                3: "Eigenmode Parameters"
#                4: "Fields"
#                5: "Far Fields"
#                6: "Near Fields"
#                7: "Emission Test"
# Display    - if Type is 1-3, then Display's possible values are::
#                1: "Rectangular Plot"
#                2: "Polar Plot"
#                3: "Radiation Pattern"
#                4: "Smith Chart"
#                5: "Data Table"
#                6: "3D Rectangular Plot"
#                7: "3D Polar Plot"
#              if Type is 4, then the possible values are::
#                1: "Rectangular Plot"
#                2: "Polar Plot"
#                3: "Radiation Pattern"
#                5: "Data Table"
#                6: "3D Rectangular Plot"
#              if Type is 5-6, then the possible values are::
#                1: "Rectangular Plot"
#                3: "Radiation Pattern" (Polar)
#                5: "Data Table"
#                6: "3D Rectangular Plot"
#                7: "3D Polar Plot"
#              if Type is 7, then the possible values are::
#                1: "Rectangular Plot"
#                5: "Data Table"
# Solution   - name of the solution given to hfssInsertSolution.
# Sweep      - name of the frequency sweep given to hfssInterpolatingSweep.
#              This can be an empty string, in which case it will be
#              used LastAdaptive instead.
# Context    - context for which the expression is being evaluated. This
#              can be an empty string if there is no context.:
#              e.g. "Infinite Sphere", "Sphere", "Polyline"
# Domain     - domain for which th expression is being evaluated. This
#              can be an empty string if there is no context.:
#              e.g. "Sweep" or "Time"
# VarObj     - cell array of names of the variables to be used as sweep
#              definitions for the report, including the frequency/ies.
#              The first one will be the primary sweep.
# DataObj    - TODO.
# 
# Note :
# ------
# This function has to be used AFTER a solution is inserted with:
# hfssInsertSolution.
#
# Example :
# ---------
# fid = fopen('myantenna.vbs', 'wt');
# / create some objects here /
# / insert far field spheres /
# hfssInsertFarFieldSphereSetup(fid, 'EPlaneCutSphere', [0 180 1], [90 90 1]);
# hfssInsertFarFieldSphereSetup(fid, 'HPlaneCutSphere', [90 90 1], [0 180 1]);
#
# hfssCreateReport(fid, 'E Plane Cut (cart.)', 5, 1, 'Solution',/
#                  ['Theta', 'Phi', 'Freq'],/
#                  ['Theta', 'dB(DirTotal)'],Context='EPlaceCutSphere');
# hfssCreateReport(fid, 'E Place Cut (polar)', 5, 3, 'Solution',/
#                  'EPlaneCutSphere', [], ['Theta', 'Phi', 'Freq'],/
#                  ['Theta', 'dB(DirTotal)']);
# hfssCreateReport(fid, 'H Plane Cut (cart.)', 5, 1, 'Solution',/
#                  'HPlaneCutSphere', [], ['Phi', 'Theta', 'Freq'],/
#                  ['Phi', 'dB(DirTotal)']);
# hfssCreateReport(fid, '3D Diagram Cart.', 5, 6, 'Solution',/
#                  'Diagram3D', [], ['Theta', 'Phi', 'Freq'],/
#                  ['Theta', 'Phi', 'dB(DirTotal)']);
# hfssCreateReport(fid, '3D Diagram Polar', 5, 7, 'Solution',/
#                  'Diagram3D', [], ['Phi', 'Theta', 'Freq'],/
#                  ['Phi', 'Theta', 'dB(DirTotal)']);
# ----------------------------------------------------------------------------
	
# ----------------------------------------------------------------------------
# CHANGELOG
#
# 25-Sept-2012: *Initial release.
# 29-Sept-2012: *Added 3D Radiation Patterns.
# 16-Janu-2013: *Fixed a bug when VarObj had only one item and wasn't
#                added to the script.
#               *Added Sweep param.
# ----------------------------------------------------------------------------
	
# ----------------------------------------------------------------------------
# Written by Daniel R. Prado
# danysan@gmail.com / drprado@tsc.uniovi.es
# 23 September 2012
# ----------------------------------------------------------------------------
def hfssCreateReport1(fid, ReportName,  Type, Display, Solution,\
	                           VarObj, DataObj,Sweep = 'LastAdaptive', Context='NULL',Domain='NULL'):
	
# Select report type string.
	ReportType = ('Modal S Parameter', 'Terminal S Parameters',\
	              'Eigenmode Parameters', 'Fields', 'Far Fields',\
	              'Near Fields', 'Emission Test');
	ReportType = ReportType[Type-1];

# Check for type and display inconsistencies
	if Type == 4 and (Display == 4 or Display == 7):
	    print('Error in hfssCreateReport 1');
	
	if (Type == 5 or Type == 6) and (Display == 2 or Display == 4):
	    print('Error in hfssCreateReport 2');
	
	if Type == 7 and ~(Display == 1 or Display == 5):
	    print('Error in hfssCreateReport 3');
	
	
# Select display type string.
	DisplayType = ('Rectangular Plot', 'Polar Plot', 'Radiation Pattern',\
	               'Smith Chart', 'Data Table', '3D Rectangular Plot',\
	               '3D Polar Plot');
	DisplayType = DisplayType[Display-1];
	
# Check for prints in VarObj
	if not((type(VarObj) is list) or  (type(VarObj) is tuple)) or len(VarObj) < 1:
	    print('Error in hfssCreateReport 4');
	
	
# Preamble.
	fid.write( '\n');
	fid.write( 'Set oModule = oDesign.GetModule("ReportSetup")\n');
	fid.write( 'oModule.CreateReport "%s", _\n'% ReportName);
	fid.write( '"%s", _\n'% ReportType);
	fid.write( '"%s", _\n'% DisplayType);
	fid.write( '"%s : %s", _\n'% (Solution, Sweep));
	
# Context parameters
	fid.write( 'Array(');
	flag = False;
	if Context != 'NULL':
	    fid.write( '"Context:=", "%s"'% Context);
	    flag = True;
	
	if Domain != 'NULL':
	    if flag:
	        fid.write( '% ');
	    
	    fid.write( '"Domain:=", "%s"'% Domain);
	
	fid.write( '), _\n');
	
# Families array parameters
	fid.write( 'Array('); # TODO: apart from "All", allow other values.
	if len(VarObj) > 1:
	    for i in range(len(VarObj)-1):
	        fid.write( '"%s:=", Array("All"), _\n'% VarObj[i]);
	    
	    fid.write( '"%s:=", Array("All")), _\n'% VarObj[i+1]);
	else:
	    fid.write( '"%s:=", Array("All")), _\n'% VarObj[0]);
	
	
# Report data array parameters.
# Deping on the Report Type, the syntax changes.
	fid.write( 'Array(');
	if Display == 1: # Rectangular plot:
	    fid.write( '"X Component:=", "%s", _\n'% DataObj[0]);
	    fid.write( '"Y Component:=", Array("%s")), _\n'% DataObj[1]);
	elif Display == 2: # Polar Plot:
	    print('Error in hfssCreateReport: display not supported');
	elif Display == 3:# Radiation Pattern:
	    fid.write( '"Ang Component:=", "%s", _\n'% DataObj[0]);
	    fid.write( '"Mag Component:=", Array("%s")), _\n'% DataObj[1]);
	elif Display == 4: # Smith Chart:
	    print('Error in hfssCreateReport: display not supported');
	elif Display == 5: # Data Table:
	    print('Error in hfssCreateReport: display not supported');
	elif Display == 6: # 3D Rectangular Plot:
	    fid.write( '"X Component:=", "%s", _\n'% DataObj[0]);
	    fid.write( '"Y Component:=", "%s", _\n'% DataObj[1]);
	    fid.write( '"Z Component:=", Array("%s")), _\n'% DataObj[2]);
	elif Display == 7: # 3D Polar Plot:
	    fid.write( '"Phi Component:=", "%s", _\n'% DataObj[0]);
	    fid.write( '"Theta Component:=", "%s", _\n'% DataObj[1]);
	    fid.write( '"Mag Component:=", Array("%s")), _\n'% DataObj[2]);
	else:
	    print('Error in hfssCreateReport: Display = wrong value');
	
	fid.write( 'Array()\n');

# ----------------------------------------------------------------------------
# function hfssExportToFile(fid, ReportName, FileName, Type):
# 
# Description :
# -------------
# Exports the report data to file, so it can be postprocesed.
#
# Parameters :
# ------------
# fid        - file identifier of the HFSS script file.:
# ReportName - name of the report to export.
# FileName   - name of the file.
# Type       - There are four possible types:
#               * txt: Post processor format file
#               * csv: Comma-delimited data file
#               * tab: Tab-separated file
#               * dat: Ansoft plot data file
#
# Note :
# ------
# In HFSS's scripting help (scripting.pdf), the example given is:
#   oDesign.ExportToFile "Plot1", "c:\report1.dat"
# However, it is wrong, since it should use oModule, instead of
# oDesign.
#
# Example :
# ---------
# hfssExportToFile(fid, 'Plot1', 'MyData', 'csv'); # Saves in the same dir.
# hfssExportToFile(fid, 'Plot2', 'C:\MyData2', 'tab');
# ----------------------------------------------------------------------------
	
# ----------------------------------------------------------------------------
# CHANGELOG
#
# 29-Sept-2012: *Initial release.
# ----------------------------------------------------------------------------
def hfssExportToFile(fid, ReportName, FileName, Type):
	
# Preamble.
	fid.write( '\n');
	fid.write( 'Set oModule = oDesign.GetModule("ReportSetup")\n');
	
# Parameters.
	fid.write( 'oModule.ExportToFile "%s", "%s.%s"\n'% (ReportName, FileName, Type));
# ----------------------------------------------------------------------------
# function hfssSaveProject(fid, projectFile, [Overwrite = false])
# 
# Description :
# -------------
# This function creates the necessary VB script to save the active HFSS 
# project onto a disk file. 
#
# Parameters :
# ------------
# fid         - file identifier of the HFSS script file.
# projectFile - full file name of the project file into which the active HFSS
#               project will be saved.
# [Overwrite] - (boolean) if set to true will overwrite any existing file with
#               the same name as that specified by projectFile.
# 
# 
# Note :
# ------
# The active HFSS project MUST be saved prior to solving it. This is slightly
# disadvantageous because we cannot create and solve projects "on-the-fly" -
# i.e., in memory without creating a project file on the disk. One workaround
# is to write the project to a temporary file and then delete the temporary
# file after the required solution is obtained.
#
# Example :
# ---------
# fid = fopen('myantenna.vbs', 'wt');

def hfssSaveProject(fid, projectFile, Overwrite = False):


# create the script.
	fid.write( '\n');
	fid.write( 'oProject.SaveAs _\n');
	fid.write( '    "%s", _\n'% projectFile);
	if Overwrite:
		fid.write( '    true\n');
	else:
		fid.write( '    false\n');


