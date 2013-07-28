from sympy.physics.mechanics import *
from sympy import sin, cos, symbols

class TestVisualizationFrameScene(object):
    
    def __init__(self):
        #We define some quantities required for tests here..
        self.p = dynamicsymbols('p:3')
        self.q = dynamicsymbols('q:3')
        self.dynamic = list(self.p) + list(self.q)
        self.states = [0 for x in self.p] + [0 for x in self.q]
        
        self.I = ReferenceFrame('I')
        self.A = self.I.orientnew('A', 'space', self.p, 'XYZ') 
        self.B = self.A.orientnew('B', 'space', self.q, 'XYZ')
        
        self.O = Point('O')
        self.P1 = self.O.locatenew('P1', 10 * self.I.x + \
                                      10 * self.I.y + 10 * self.I.z)
        self.P2 = self.P1.locatenew('P2', 10 * self.I.x + \
                                    10 * self.I.y + 10 * self.I.z)
        
        self.point_list1 = [[2, 3, 1], [4, 6, 2], [5, 3, 1], [5, 3, 6]]
        self.point_list2 = [[3, 1, 4], [3, 8, 2], [2, 1, 6], [2, 1, 1]]

        #any random simple shape .. 
        #TODO replace by a mesh shape ideally, when its implemented
        self.mesh_shape1 = Cylinder()
        self.mesh_shape2 = Cylinder()
                               
                               
        self.Ixx, self.Iyy, self.Izz = symbols('Ixx Iyy Izz')
        self.mass = symbols('mass')
        self.parameters = [self.Ixx, self.Iyy, self.Izz, self.mass]
        self.param_vals = [0, 0, 0, 0] 
        
        self.inertia = inertia(self.A, self.Ixx, self.Iyy, self.Izz)

        self.rigid_body = RigidBody('rigid_body1', self.P1, self.A, \
                                 self.mass, (self.inertia, self.P1))
        
        self.global_frame1 = VisualizationFrame('global_frame1', \
                                self.A, self.P1, shape=self.mesh_shape1)                  
                                 
        self.global_frame2 = VisualizationFrame('global_frame2', \
                                self.B, self.P2, shape=self.mesh_shape2)                  

        self.particle = Particle('particle1', self.P1, self.mass)                            
        
        #To make it more readable      
        p = self.p
        q = self.q 
        #Here is the dragon ..
        self.transformation_matrix = \
            [[cos(p[1])*cos(p[2]), sin(p[2])*cos(p[1]), -sin(p[1]), 0], \
             [sin(p[0])*sin(p[1])*cos(p[2]) - sin(p[2])*cos(p[0]), \
                  sin(p[0])*sin(p[1])*sin(p[2]) + cos(p[0])*cos(p[2]), \
                  sin(p[0])*cos(p[1]), 0], \
             [sin(p[0])*sin(p[2]) + sin(p[1])*cos(p[0])*cos(p[2]), \
                 -sin(p[0])*cos(p[2]) + sin(p[1])*sin(p[2])*cos(p[0]), \
                  cos(p[0])*cos(p[1]), 0], \
             [10, 10, 10, 1]]
    
    
    def test_vframe_with_rframe(self):
        self.frame1 = VisualizationFrame('frame1', self.I, self.O, \
                                                shape=self.mesh_shape1)
    
        assert self.frame1.name == 'frame1'
        assert self.frame1.reference_frame == self.I
        assert self.frame1.origin == self.O
        assert self.frame1.shape is self.mesh_shape1
        
        self.frame1.name = 'frame1_'
        assert self.frame1.name == 'frame1_'
        
        self.frame1.reference_frame = self.A
        assert self.frame1.reference_frame == self.A
        
        self.frame1.origin = self.P1
        assert self.frame1.origin == self.P1
        
        self.frame1.shape = self.mesh_shape2
        assert self.frame1.shape is self.mesh_shape2    
        
        assert self.frame1.transform(self.I, self.O).tolist() == \
                                             self.transformation_matrix


    def test_vframe_with_rbody(self):
        self.frame2 = VisualizationFrame('frame2', self.rigid_body, \
                                                shape=self.mesh_shape1)
        
        assert self.frame2.name == 'frame2'
        assert self.frame2.reference_frame == self.A
        assert self.frame2.origin == self.P1
        assert self.frame2.shape == self.mesh_shape1
        
        self.frame2.name = 'frame2_'
        assert self.frame2.name == 'frame2_'
        
        self.frame2.reference_frame = self.B
        assert self.frame2.reference_frame == self.B
        
        self.frame2.origin = self.P2
        assert self.frame2.origin == self.P2
        
        self.frame2.shape = self.mesh_shape2
        assert self.frame2.shape is self.mesh_shape2    

        self.frame2.reference_frame = self.A
        self.frame2.origin = self.P1
        assert self.frame2.transform(self.I, self.O).tolist() == \
                                            self.transformation_matrix
                                            


    def test_vframe_with_particle(self):
        
        self.frame3 = VisualizationFrame('frame3', \
                                          self.particle, self.A, \
                                                shape=self.mesh_shape1)
        
        assert self.frame3.name == 'frame3'
        assert self.frame3.reference_frame == self.A
        assert self.frame3.origin == self.P1
        assert self.frame3.shape is self.mesh_shape1
        
        self.frame3.name = 'frame3_'
        assert self.frame3.name == 'frame3_'
        
        self.frame3.reference_frame = self.B
        assert self.frame3.reference_frame == self.B
        
        self.frame3.origin = self.P2
        assert self.frame3.origin == self.P2
        
        self.frame3.shape = self.mesh_shape2
        assert self.frame3.shape is self.mesh_shape2        

        self.frame3.reference_frame = self.A
        self.frame3.origin = self.P1
        assert self.frame3.transform(self.I, self.O).tolist() == \
                                             self.transformation_matrix

    def test_vframe_without_name(self):
        self.frame4 = VisualizationFrame(self.I, self.O, \
                                               shape=self.mesh_shape1)
        
        assert self.frame4.name == 'UnNamed'
        #To check if referenceframe and origin are defined 
        #properly without name arg
        assert self.frame4.reference_frame == self.I 
        assert self.frame4.origin == self.O
        assert self.frame4.shape is self.mesh_shape1
        
        self.frame4.name = 'frame1_'
        assert self.frame4.name == 'frame1_'
    
    def test_vframe_nesting(self):
        self.frame5 = VisualizationFrame('parent-frame', self.I, \
                                        self.O, shape=self.mesh_shape1)
        
        self.frame5.add_child_frames(self.global_frame1, \
                                          self.global_frame2)
                                                                                                            
        assert self.frame5.child_frames[0] is self.global_frame1
        assert self.frame5.child_frames[1] is self.global_frame2
        
        self.frame5.remove_child_frames(self.global_frame1, \
                                                  self.global_frame2)
        
        assert len(self.frame5.child_frames) == 0                                           

    def test_numeric_transform(self):
        self.list1 = [[1.0, 0.0, 0.0, 0.0], \
                      [0.0, 1.0, 0.0, 0.0], \
                      [0.0, 0.0, 1.0, 0.0], \
                      [10.0, 10.0, 10.0, 1.0]]
        
        self.list2 = [[1.0, 0.0, 0.0, 0.0], \
                      [0.0, 1.0, 0.0, 0.0], \
                      [0.0, 0.0, 1.0, 0.0], \
                      [20.0, 20.0, 20.0, 1.0]]
                      

        self.global_frame1.transform(self.I, self.O)
        self.global_frame1.generate_numeric_transform(self.dynamic, \
                                                        self.parameters)
        
        assert self.global_frame1.evaluate_numeric_transform(self.states, \
                                       self.param_vals).tolist() == \
                                       self.list1
        
        self.global_frame2.transform(self.I, self.O)
        self.global_frame2.generate_numeric_transform(self.dynamic, \
                                                        self.parameters)
        
        assert self.global_frame2.evaluate_numeric_transform(self.states, \
                                       self.param_vals).tolist() == \
                                       self.list2
        
                   
    def test_camera(self):
        #Camera is a subclass of VisualizationFrame, but without any
        #specific shape attached. We supply only ReferenceFrame,Point
        #to camera. and it inherits methods from VisualizationFrame
        camera = Camera('camera', self.I, self.O)
        
        assert camera.name == 'camera'
        assert camera.reference_frame == self.I
        assert camera.origin == self.O
        
        camera.name = 'camera1'
        assert camera.name == 'camera1'
        
        camera.reference_frame = self.A
        assert camera.reference_frame == sel.A
        
        camera.origin = self.P1
        assert camera.origin == self.P1
        
        #We can check transformation matrix for camera, in the extended 
        #example.
        
        #UnNamed camera
        camera1 = Camera(self.I, self.O)
        assert camera1.name == 'UnNamed'
        assert camera1.reference_frame == self.I
        assert camera1.origin == self.O

    def test_scene(self):
        self.scene = Scene('scene', self.I, self.O)
        self.scene.add_visualization_frames(self.frame1, self.frame2, \
                                                      self.frame3)
        assert self.scene.name == 'scene'                                                      
        assert self.scene.reference_frame == self.I
        assert self.scene.origin == self.O
        assert self.scene.get_visualization_frames[0] is self.frame1
        assert self.scene.get_visualization_frames[1] is self.frame2
        assert self.scene.get_visualization_frames[2] is self.frame3
        
        
        self.scene.name = 'scene1'
        assert self.scene.name == 'scene1'
        
        self.scene.reference_frame = self.A
        assert self.scene.reference_frame == self.A
        
        self.scene.remove_frame(self.frame1)
        assert self.scene.frames[0] is self.frame2
        assert self.scene.frames[1] is self.frame3
        
        self.scene.add_visualization_frame(self.frame1)
        assert self.scene.frames[0] is self.frame1
        assert self.scene.frames[1] is self.frame2
        assert self.scene.frames[2] is self.frame3
        #TODO check for multiple frame insertion 
        #add_visualization_frames
