# # Fault

from LoopStructural.interpolators.piecewiselinear_interpolator import PiecewiseLinearInterpolator as PLI
from LoopStructural.supports.tet_mesh import TetMesh
from LoopStructural.modelling.features.geological_feature import GeologicalFeatureInterpolator
from LoopStructural.modelling.features.faulted_geological_feature import FaultedGeologicalFeature
from LoopStructural.visualisation.model_visualisation import LavaVuModelViewer
from LoopStructural.modelling.features.structural_frame import StructuralFrameBuilder
from LoopStructural.modelling.fault.fault_segment import FaultSegment
import numpy as np

boundary_points = np.zeros((2,3))

boundary_points[0,0] = -20
boundary_points[0,1] = -20
boundary_points[0,2] = -20
boundary_points[1,0] = 20
boundary_points[1,1] = 20
boundary_points[1,2] = 20
mesh = TetMesh()
mesh.setup_mesh(boundary_points, nstep=1, n_tetra=40000,)

interpolator = PLI(mesh)
stratigraphy_builder = GeologicalFeatureInterpolator(interpolator=interpolator, name='stratigraphy')


stratigraphy_builder.add_point([6.1,0.1,1.1],0.)


stratigraphy_builder.add_strike_and_dip([1,1,1],90.,0.)
stratigraphy = stratigraphy_builder.build(solver='lu',cgw=.1)




floor = -6
roof = 6
fault_interpolator = PLI(mesh)
fault = StructuralFrameBuilder(interpolator=fault_interpolator,mesh=mesh,name='FaultSegment1')
for y in range(-20,20,1):
    fault.add_strike_dip_and_value([-15.17,y,floor],strike=0.,dip=0.,val=0,itype='gx')
    fault.add_strike_dip_and_value([-6.17,y,floor],strike=0.,dip=0.,val=0,itype='gx')
    # fault.add_strike_dip_and_value([-4.,y,floor],strike=0.,dip=45.,val=0,itype='gx')
    fault.add_strike_dip_and_value([6.17,y,roof],strike=0.,dip=0.,val=0,itype='gx')
    fault.add_strike_dip_and_value([4.,y,roof],strike=0.,dip=0.,val=0,itype='gx')
    fault.add_strike_dip_and_value([8.17,y,roof],strike=0.,dip=0.,val=0,itype='gx')
    fault.add_strike_dip_and_value([15.17,y,roof],strike=0.,dip=0.,val=0,itype='gx')


fault.add_point([2.5,19,1.5],0.,itype='gz')
fault.add_point([2.5,-19,1.5],1.,itype='gz')
for y in range(-20,20,1):
    fault.add_point([-10.5,y,floor],0.,itype='gy')
    fault.add_point([11.56,y,roof],1.,itype='gy')


fault_frame = fault.build(solver='lu',gxxgy=0.1,gxxgz=1,gyxgz=0.05,gycg=5,gzcg=0.1)

fault_operator = FaultSegment(
                    fault_frame,
                    displacement=-4
                              )


faulted_feature = FaultedGeologicalFeature(stratigraphy, fault_operator)
viewer = LavaVuModelViewer()
# viewer.plot_isosurface(
#     faulted_feature.hw_feature,
#     nslices=10,
#     paint_with=faulted_feature.feature
# )
viewer.add_isosurface(
    faulted_feature,
    nslices=10,
    voxet={'bounding_box':boundary_points,'nsteps':(50,50,25)},
    paint_with=faulted_feature
)
viewer.add_isosurface(fault_frame.features[0], isovalue=0, colour='blue')

viewer.save('03_ramp_flat_fault.png')
