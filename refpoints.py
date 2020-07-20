import re
import numpy as np
class REFPOINTS:
    def __init__(self, b_ref, c_ref, b_real, c_real):
        self.a_ref = np.array([0,0,0])
        self.b_ref = b_ref
        self.c_ref = c_ref
        self.a_real = np.array([0,0,0])
        self.b_real = b_real
        self.c_real = c_real
        self.check_geometry()
        self.rot_matrix = self.calc_rot_matrix()

    def check_geometry(self):
        self.ab_ref = np.linalg.norm(self.b_ref)
        self.ac_ref = np.linalg.norm(self.c_ref)
        self.bc_ref = np.linalg.norm(self.b_ref-self.c_ref)
        self.ab_real = np.linalg.norm(self.b_real-self.a_real)
        self.ac_real = np.linalg.norm(self.c_real-self.a_real)
        self.bc_real = np.linalg.norm(self.b_real-self.c_real)
        print("ab_ref: ",self.ab_ref)
        print("ac_ref: ",self.ac_ref)
        print("bc_ref: ",self.bc_ref)
        print("ab_real ",self.ab_real)
        print("ac_real ",self.ac_real)
        print("bc_real ",self.bc_real)
        assert(np.abs((self.ab_ref - self.ab_real)/self.ab_ref)<=0.03)
        assert(np.abs((self.ac_ref - self.ac_real)/self.ac_ref)<=0.03)
        assert(np.abs((self.bc_ref - self.bc_real)/self.bc_ref)<=0.03)

    def calc_rot_matrix(self):
        rot1_axis = np.cross(self.b_ref,self.b_real)
        rot1_axis = rot1_axis/(np.linalg.norm(rot1_axis))
        theta = np.arccos(np.dot(self.b_ref,self.b_real)/(self.ab_ref*self.ab_real))
        #TODO: compare distance instead.
        # rot_matrix1 = self.axis_rot(rot1_axis, theta)
        # b_ref_rot = rot_matrix1.dot(self.b_ref)
        # if (np.linalg.norm(b_ref_rot-self.b_real) > 0.03*self.ab_real):
        #         rot_matrix1 = self.axis_rot(rot1_axis, -1*theta)
        # b_ref_rot = rot_matrix1.dot(self.b_ref)
        rot_matrix1_p = self.axis_rot(rot1_axis, theta)
        rot_matrix1_n = self.axis_rot(rot1_axis, -1*theta)
        b_ref_rot_p = rot_matrix1_p.dot(self.b_ref)
        b_ref_rot_n = rot_matrix1_n.dot(self.b_ref)
        if np.linalg.norm(b_ref_rot_p-self.b_real) <= np.linalg.norm(b_ref_rot_n-self.b_real):
            rot_matrix1 = self.axis_rot(rot1_axis, theta)
        else:
            rot_matrix1 = self.axis_rot(rot1_axis, -1*theta)
        b_ref_rot = rot_matrix1.dot(self.b_ref)
        print(np.linalg.norm(b_ref_rot-self.b_real))
        assert(np.linalg.norm(b_ref_rot-self.b_real) < 0.03*self.ab_real)

        rot2_axis = self.b_real/(self.ab_real)
        c_ref_rot = rot_matrix1.dot(self.c_ref)

        v1 = c_ref_rot - np.dot(c_ref_rot,rot2_axis)*rot2_axis
        v2 = self.c_real - np.dot(self.c_real,rot2_axis)*rot2_axis
        theta = np.arccos(np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)))

        rot_matrix2_p = self.axis_rot(rot2_axis, theta)
        rot_matrix2_n = self.axis_rot(rot2_axis, -1*theta)
        c_ref_rot2_p = rot_matrix2_p.dot(c_ref_rot)
        c_ref_rot2_n = rot_matrix2_n.dot(c_ref_rot)
        if np.linalg.norm(c_ref_rot2_p-self.c_real) <= np.linalg.norm(c_ref_rot2_n-self.c_real):
            rot_matrix2 = self.axis_rot(rot2_axis, theta)
        else:
            rot_matrix2 = self.axis_rot(rot2_axis, -1*theta)
        c_ref_rot2 = rot_matrix2.dot(c_ref_rot)
        assert(np.linalg.norm(c_ref_rot2-self.c_real) < 0.03*self.ac_real)

        # rot_matrix2 =  self.axis_rot(rot2_axis, theta)
        # c_ref_rot2 = rot_matrix2.dot(c_ref_rot)
        # if (np.linalg.norm(c_ref_rot2-self.c_real) > 0.03*self.ac_real):
        #         rot_matrix2 = self.axis_rot(rot2_axis, -1*theta)
        # c_ref_rot2 = rot_matrix2.dot(c_ref_rot)
        # assert(np.linalg.norm(c_ref_rot2-self.c_real) < 0.03*self.ac_real)

        rot_matrix = np.matmul(rot_matrix2,rot_matrix1)
        assert(np.linalg.norm(rot_matrix.dot(self.c_ref)-self.c_real) < 0.03*self.ac_real)
        assert(np.linalg.norm(rot_matrix.dot(self.b_ref)-self.b_real) < 0.03*self.ab_real)
        return rot_matrix

    def axis_rot(self, axis, theta):
        np.testing.assert_approx_equal(1.0, np.linalg.norm(axis))
        matrix = np.zeros((3,3))
        matrix[0,0] = np.cos(theta) + axis[0]**2*(1-np.cos(theta))
        matrix[0,1] = axis[0]*axis[1]*(1-np.cos(theta)) - axis[2]*np.sin(theta)
        matrix[0,2] = axis[0]*axis[2]*(1-np.cos(theta)) + axis[1]*np.sin(theta)
        matrix[1,0] = axis[0]*axis[1]*(1-np.cos(theta)) + axis[2]*np.sin(theta)
        matrix[1,1] = np.cos(theta) + axis[1]**2*(1-np.cos(theta))
        matrix[1,2] = axis[1]*axis[2]*(1-np.cos(theta)) - axis[0]*np.sin(theta)
        matrix[2,0] = axis[0]*axis[2]*(1-np.cos(theta)) - axis[1]*np.sin(theta)
        matrix[2,1] = axis[1]*axis[2]*(1-np.cos(theta)) + axis[0]*np.sin(theta)
        matrix[2,2] = np.cos(theta) + axis[2]**2*(1-np.cos(theta))
        return matrix
