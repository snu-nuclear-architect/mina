import math
import numpy as np
from scipy import interpolate
class pipe:
    def __init__(self, name, type_name, length, diameter, orientation, surfaceroughness, subnodes_number):

        """
        Generate inherent property of pipe.

        Keyword arguments:
        name              -- the name of this component                                                           ~
        type              -- the type of this class                                                               ["pipe" / "ring pipe"]
        length            -- the length of the pipe                                                               [m]
        diameter          -- the diameter of the pipe /
                            [diameter of the outer pipe, diameter of the inner pip   [m]
        orientation       -- the orientation of the pipe                                                          ["verical" / "horizontal"]
        surfaceroughness  -- the surfaceroughness                                                                 [m]
        subnodes_numbers  __ the subnodes numbers                                                                 ~
        """
        self.name              = name
        self.type              = type_name
        self.length            = length
        self.diameter          = diameter
        self.orientation       = orientation
        self.surfaceroughness  = surfaceroughness
        self.subnodes_number   = subnodes_number

    def Theta(self):
        if self.orientation == "vertical":
            self.theta         = 0
        if self.orientation == "horizontal":
            self.theta         = math.pi / 2

    def HyD(self):
        if self.type == "pipe":
            self.Dh            = self.diameter
        if self.type == "ring pipe":
            self.Dh            = 4 * (math.pi * (self.diameter[0] ** 2 - self.diameter[1] ** 2) / 4) / (math.pi * self.diameter[0] + math.pi * self.diameter[1])

    def V_ref(self):
        if self.type == "pipe":
            self.v_ref         = self.mass_flow_rate / (self.rho_ref * math.pi * self.diameter ** 2 / 4)
        if self.type == "ring pipe":
            self.v_ref         = self.mass_flow_rate / (self.rho_ref * math.pi * (self.diameter[0] ** 2 - self.diameter[1] ** 2) / 4)

    def fric_f(self):
        if self.Re > 3000:
            self.f             = (1/(-2 * math.log10(self.surfaceroughness/ ( 3.7 * self.Dh ) + 2.51 / self.Re * ( 1.14 - 2 * math.log10( math.fabs(self.surfaceroughness / self.Dh - 21.25 / self.Re**0.9 )) ) )))**2
        if self.Re < 2000:
            self.f             = 64 / self.Re
        if self.Re >= 2000 and self.Re <= 3000:
            self.f             = (3.75-8250/self.Re) * ( (1/(-2 * math.log10(self.surfaceroughness / ( 3.7 * self.Dh ) + 2.51 / 3000 * ( 1.14 - 2 * math.log10( math.fabs(self.surfaceroughness / self.Dh - 21.25 / 3000**0.9 )) ) )))**2 - 64 / 2200 ) + 64 / 2200


    def calculation(self, inletcondition):
        self.Theta()
        self.T_in              = inletcondition.T_out
        self.mass_flow_rate_in = inletcondition.mass_flow_rate_out
        self.P_in              = inletcondition.P_out

        self.T_ref             = self.T_in
        self.P_ref             = self.P_in
        self.mass_flow_rate    = self.mass_flow_rate_in

        self.rho_ref           = 11047-1.2564*self.T_ref
        self.mu                = 4.94e-4 * math.exp(754.1/self.T_ref)
        self.HyD()
        self.V_ref()
        self.Re                = self.v_ref * self.Dh * self.rho_ref / self.mu
        self.fric_f()
        self.P_out             =  self.P_in - self.rho_ref*(9.8 * self.length * math.cos(self.theta) + self.f*self.length/self.Dh*self.v_ref**2. / 2.)
        self.T_out             = self.T_ref
        self.mass_flow_rate_out= self.mass_flow_rate_in


class orifice:
    def __init__(self, name, type_name, length, diameter, orientation, surfaceroughness, hole_diameter):

        """
        Generate inherent property of pipe.

        Keyword arguments:
        name              -- the name of this component     ~
        type              -- the type of this class         ["orifice"]
        length            -- the length of the pipe         [m]
        diameter          -- the diameter of the pipe       [m]
        orientation       -- the orientation of the pipe    ["verical" / "horizontal"]
        surfaceroughness  -- the surfaceroughness           [m]
        hole_diameter     __ the hole diameter              [m]
        """
        self.name              = name
        self.type              = type_name
        self.length            = length
        self.diameter          = diameter
        self.orientation         = orientation
        self.surfaceroughness  = surfaceroughness
        self.hole_diameter     = hole_diameter

    def theta(self):
        if self.orientation == "vertical":
            self.theta          = 0
        if self.orientation == "horizontal":
            self.theta          = math.pi / 2
            
    def fric_f(self):
        if self.Re > 3000:
            self.f              = (1/(-2 * math.log10(self.surfaceroughness/ ( 3.7 * self.Dh ) + 2.51 / self.Re * ( 1.14 - 2 * math.log10( math.fabs(self.surfaceroughness / self.Dh - 21.25 / self.Re**0.9 )) ) )))**2
        if self.Re < 2000:
            self.f              = 64 / self.Re
        if self.Re >= 2000 and self.Re <= 3000:
            self.f              = (3.75-8250/self.Re) * ( (1/(-2 * math.log10(self.surfaceroughness / ( 3.7 * self.Dh ) + 2.51 / 3000 * ( 1.14 - 2 * math.log10( math.fabs(self.surfaceroughness / self.Dh - 21.25 / 3000**0.9 )) ) )))**2 - 64 / 2200 ) + 64 / 2200

    def calculation(self, inletcondition):
        self.theta()
        self.T_in               = inletcondition.T_out
        self.mass_flow_rate_in  = inletcondition.mass_flow_rate_out
        self.P_in               = inletcondition.P_out

        self.T_ref              = self.T_in
        self.P_ref              = self.P_in
        self.mass_flow_rate     = self.mass_flow_rate_in

        self.rho_ref            = 11047-1.2564*self.T_ref
        self.mu                 = 4.94e-4 * math.exp(754.1/self.T_ref)
        self.v_ref              = self.mass_flow_rate_in / (self.rho_ref * math.pi * self.diameter ** 2 / 4)
        self.Dh                 = self.diameter
        self.Re                 = self.v_ref * self.Dh * self.rho_ref / self.mu
        self.fric_f()
        self.A                  = math.pi * self.diameter ** 2 / 4
        self.A_hole             = math.pi * self.hole_diameter ** 2 / 4
        self.k                  = (1 + 0.707 * ( 1 - self.A_hole / self.A )**0.375 - self.A_hole / self.A )**2 * ( self.A / self.A_hole )**2
        self.P_out              = self.P_in - self.rho_ref * (9.8 * self.length * math.cos(self.theta) + 0.5 * self.k * self.v_ref ** 2 + self.f * self.length / self.Dh * self.v_ref**2 / 2)
        self.T_out              = self.T_ref
        self.mass_flow_rate_out = self.mass_flow_rate_in

class sudden_change:
    def __init__(self, name, type_name, upstream_diameter_or_area, downstream_diameter_or_area):

        """
        Generate inherent property of sudden_change.

        Keyword arguments:
        name                    -- the name of this component     ~
        type                    -- the type of this class         ["sudden expansion" / "sudden expansion (area)" / "sudden expansion" / "sudden expansion (area)"]
        upstream_diameter       -- the diameter of the pipe       [m]
        downstream_diameter     __ the hole diameter              [m]
        """
        self.name                           = name
        self.type                           = type_name
        self.length                         = 0
        self.upstream_diameter_or_area      = upstream_diameter_or_area
        self.downstream_diameter_or_area    = downstream_diameter_or_area

    def calculation(self, inletcondition):
        self.T_in                   = inletcondition.T_out
        self.mass_flow_rate_in      = inletcondition.mass_flow_rate_out
        self.P_in                   = inletcondition.P_out

        self.T_ref                  = self.T_in
        self.P_ref                  = self.P_in
        self.mass_flow_rate         = self.mass_flow_rate_in

        self.rho_ref                = 11047-1.2564*self.T_ref
        self.mu                     = 4.94e-4 * math.exp(754.1/self.T_ref)
        if self.type  == "sudden expansion":
            self.v_ref                  = self.mass_flow_rate / (self.rho_ref * math.pi * self.upstream_diameter_or_area ** 2 / 4)
        if self.type  == "sudden contraction":
            self.v_ref                  = self.mass_flow_rate / (self.rho_ref * math.pi * self.downstream_diameter_or_area ** 2 / 4)
        if self.type  == "sudden expansion (area)":
            self.v_ref                  = self.mass_flow_rate / (self.rho_ref * self.upstream_diameter_or_area)
        if self.type  == "sudden contraction (area)":
            self.v_ref                  = self.mass_flow_rate / (self.rho_ref * self.downstream_diameter_or_area)
        if self.type  == "sudden expansion" or self.type == "sudden contraction":
            self.upstream_area          = math.pi * ( self.upstream_diameter_or_area / 2 ) ** 2
            self.downstream_area        = math.pi * ( self.downstream_diameter_or_area / 2 ) ** 2
        if self.type  == "sudden expansion (area)" or self.type == "sudden contraction (area)":
            self.upstream_area          = self.upstream_diameter_or_area
            self.downstream_area        = self.downstream_diameter_or_area

        if self.type  == "sudden expansion" or self.type == "sudden expansion (area)":
            self.k                  = (1 - self.upstream_area / self.downstream_area ) ** 2
        if self.type  == "sudden contraction" or self.type == "sudden contraction (area)":
#           self.k                  = ( 1 - 1 / ( 0.62 + 0.38 * ( self.downstream_area / self.upstream_area )**3 ) )**2
            self.k                  = 0.5-0.7 * (self.downstream_area / self.upstream_area ) + 0.2 * (self.downstream_area / self.upstream_area )**2
        self.P_out                  = self.P_in - self.rho_ref * ( 0.5 * self.k * self.v_ref**2.)
        self.T_out                  = self.T_ref
        self.mass_flow_rate_out     = self.mass_flow_rate_in
"""

class sudden_contraction():
    def __init__(self, type_name, upstream_diameter, downstream_diameter):



#        Generate inherent property of pipe.

#        Keyword arguments:
 #       type                    -- the type of this class         ["sudden expansion"]
  #      upstream_diameter       -- the diameter of the pipe       [m]
   #     downstream_diameter     __ the hole diameter              [m]

        self.type                   = type_name
        self.upstream_diameter      = upstream_diameter
        self.downstream_diameter    = downstream_diameter

    def k_turbulence(self):
        ratio_of_area = np.array([0,0.2,0.4,0.6,0.8,0.9,1.0])



    def calculation(self, inletcondition):
        self.T_in                   = inletcondition.T_out
        self.mass_flow_rate_in      = inletcondition.mass_flow_rate_out
        self.P_in                   = inletcondition.P_out

        self.T_ref                  = self.T_in
        self.P_ref                  = self.P_in
        self.mass_flow_rate         = self.mass_flow_rate_in

        self.rho_ref                = 11047-1.2564*self.T_ref
        self.mu                     = 4.94e-4 * math.exp(754.1/self.T_ref)
        self.upstream_area          = math.pi * ( self.upstream_diameter / 2 ) ** 2
        self.downstream_area        = math.pi * ( self.downstream_diameter / 2 ) ** 2
        self.v_ref                  = self.mass_flow_rate / (self.rho_ref * self.downstream_area )
        self.Dh                     = self.downstream_diameter
        self.Re                     = self.v_ref * self.Dh * self.rho_ref / self.mu

        if self.Re > 1e4:





        self.P_out                  = self.P_in - self.rho_ref * ( 0.5 * self.k * self.v_ref**2.)
        self.T_out                  = self.T_ref
        self.mass_flow_rate_out     = self.mass_flow_rate_in
"""
class gate_valve:
    def __init__(self, name, type_name, length, diameter, gate_diameter, orientation):

        """
        Generate inherent property of pipe.

        Keyword arguments:
        name              -- the name of this component     ~
        type              -- the type of this class         ["gate valve"]
        length            -- the length of the gate valve   [m]
        diameter          -- the diameter of the pipe       [m]
        orientation         -- the orientation of the pipe  ["verical" / "horizontal"]
        surfaceroughness  -- the surfaceroughness           [m]
        hole_diameter     __ the hole diameter              [m]
        """
        self.name                    = name
        self.type                    = type_name
        self.length                  = length
        self.diameter                = diameter
        self.orientation             = orientation
        self.gate_diameter           = gate_diameter

    def theta(self):
        if self.orientation == "vertical":
            self.theta          = 0
        if self.orientation == "horizontal":
            self.theta          = math.pi / 2

    def calculation(self, inletcondition):
        self.theta()
        self.T_in                   = inletcondition.T_out
        self.mass_flow_rate_in      = inletcondition.mass_flow_rate_out
        self.P_in                   = inletcondition.P_out
        self.T_ref                  = self.T_in
        self.P_ref                  = self.P_in
        self.mass_flow_rate         = self.mass_flow_rate_in
        self.rho_ref                = 11047-1.2564*self.T_ref
        self.mu                     = 4.94e-4 * math.exp(754.1/self.T_ref)
        self.v_ref1                 = self.mass_flow_rate / (self.rho_ref * math.pi * self.gate_diameter ** 2 / 4)
        self.v_ref2                 = self.mass_flow_rate / (self.rho_ref * math.pi * self.gate_diameter ** 2 / 4)
        self.area1                  = math.pi * ( self.diameter / 2 ) ** 2
        self.area2                  = math.pi * ( self.gate_diameter / 2 ) ** 2
#        self.k1                     = ( 1 - 1 / ( 0.62 + 0.38 * ( self.area2 / self.area1 )**3 ) )**2
        self.k1                     = 0.5-0.7 * (self.area2 / self.area1 ) + 0.2 * (self.area2 / self.area1 )**2
        self.k2                     = (1 -  self.area2 / self.area1 ) ** 2
        self.P_out                  = self.P_in - self.rho_ref * ( 0.5 * self.k1 * self.v_ref1**2) - self.rho_ref * ( 0.5 * self.k2 * self.v_ref2**2) - self.rho_ref * (9.8 * self.length * math.cos(self.theta))
        self.T_out                  = self.T_ref
        self.mass_flow_rate_out     = self.mass_flow_rate_in

class elbow:
    def __init__(self, name, type_name, diameter, radius_of_curvature, elbow_angle, orientation, surface_roughness):

        """
        Generate inherent property of pipe.

        Keyword arguments:
        name                -- the name of this component     ~
        type                -- the type of this class         ["elbow"]
        diameter            -- pipe diameter                  [m]
        radius_of_curvature -- radius_of_curvature            [m]
        orientation         -- the orientation of the pipe    ["verical" / "horizontal"]
        surfaceroughness    -- the surfaceroughness           [m]
        elbow_angle         -- the elbow angle                [degree]
        """
        self.name                    = name
        self.type                    = type_name
        self.diameter                = diameter
        self.radius_of_curvature     = radius_of_curvature
        self.orientation             = orientation
        self.surface_roughness       = surface_roughness
        self.elbow_angle             = elbow_angle
        self.RperD                   = radius_of_curvature / diameter
        self.surface_roughnessratio  = surface_roughness / diameter
        
    def theta(self):
        if self.orientation == "vertical":
            self.theta          = 0
        if self.orientation == "horizontal":
            self.theta          = math.pi / 2
            
    def fun_kre(self,a,b):
        D = { 0.10:[1.40,1.67,2.00], 0.14:[1.33,1.58,1.89], 0.2:[1.26,1.49,1.77], 0.3:[1.19,1.40,1.64], 0.4:[1.14,1.34,1.56], 0.6:[1.09,1.26,1.46], 0.8:[1.06,1.21,1.38], 1.0:[1.04,1.19,1.30], 1.4:[1.0,1.17,1.15], 2.0:[1.0,1.14,1.02], 3.0:[1.0,1.06,1.0], 4.0:[1.0,1.0,1.0]  }
        if a*1e-5 in D.keys():
            if 0.5<=b<=0.55:
                self.kre            = D[a*1e-5][0]
            if 0.55<b<=0.70:
                self.kre            = D[a*1e-5][1]
            if b>0.70:
                self.kre            = D[a*1e-5][2]
    
        else:
            if 0.5<=b<=0.55:
                self.kre            = 1 + 4400./a
            if 0.55<b<=0.70:
                self.kre            = 5.45/(a**0.131)
            if b>0.70:
                self.kre            = 1.3 - 0.29 * math.log(a * 1e-5,math.e)

    def fun_A1(self):
            elbow_anglex            = np.array([20,30,45,60,75,90,110,130,150,180])
            A1_value                = np.array([0.31,0.45,0.60,0.78,0.90,1.0,1.13,1.20,1.28,1.40])
            A1_fun                  = interpolate.interp1d(elbow_anglex,A1_value,kind='linear')
            self.A1                 = float(A1_fun(self.elbow_angle))

    def fun_B1(self):
            RperDx                  = np.array([0.50,0.60,0.70,0.80,0.90,1.00,1.25,1.50,2.00,4.00])
            B1_value                = np.array([1.18,0.77,0.51,0.37,0.28,0.21,0.19,0.17,0.15,0.11])
            B1_fun                  = interpolate.interp1d(RperDx,B1_value,kind='linear')
            self.B1                 = float(B1_fun(self.RperD))
    def fun_lambda(self):
            Rex                     = np.array([3e3,4e3,6e3,1e4,2e4,4e4,6e4,1e5,2e5])
            surface_roughness_ratio = np.array([0.0008,0.0006,0.0004,0.0002,0.0001,0.00005,0.00001,0.000005])
            lambdaz                 = np.array([[0.043,0.040,0.036,0.032,0.027,0.024,0.023,0.022,0.020],
                                                [0.046,0.040,0.036,0.032,0.027,0.023,0.022,0.021,0.018],
                                                [0.036,0.040,0.036,0.032,0.027,0.023,0.022,0.020,0.018],
                                                [0.036,0.040,0.036,0.032,0.027,0.022,0.021,0.019,0.017],
                                                [0.036,0.040,0.036,0.032,0.027,0.022,0.021,0.019,0.017],
                                                [0.036,0.040,0.036,0.032,0.027,0.022,0.021,0.019,0.016],
                                                [0.036,0.040,0.036,0.032,0.027,0.022,0.021,0.019,0.016],
                                                [0.036,0.040,0.036,0.032,0.027,0.022,0.021,0.019,0.016],])
            lambda_fun              = interpolate.interp2d(Rex,surface_roughness_ratio,lambdaz,kind='linear')
            self.lambda_value       = float(lambda_fun(self.Re,self.surface_roughnessratio))


    def calculation(self, inletcondition):
        self.theta()
        self.T_in                   = inletcondition.T_out
        self.mass_flow_rate_in      = inletcondition.mass_flow_rate_out
        self.P_in                   = inletcondition.P_out
        self.T_ref                  = self.T_in
        self.P_ref                  = self.P_in
        self.mass_flow_rate         = self.mass_flow_rate_in
        self.rho_ref                = 11047-1.2564*self.T_ref
        self.mu                     = 4.94e-4 * math.exp(754.1/self.T_ref)        
        self.length                 = self.radius_of_curvature * math.sin(self.elbow_angle)
        self.v_ref                  = self.mass_flow_rate / ( self.rho_ref * math.pi * (self.diameter / 2) ** 2 )
        self.Re                     = self.v_ref * self.rho_ref * self.diameter / self.mu
        self.fun_kre(self.Re,self.radius_of_curvature/self.diameter)
        self.fun_A1()
        self.fun_B1()
        self.fun_lambda()
        self.K_loc                  = self.A1 * self.B1
        self.K_fr                   = 0.0175 * self.radius_of_curvature / self.diameter * self.elbow_angle *self.lambda_value
        self.fun_kre(self.Re, self.radius_of_curvature / self.diameter)
        self.K                      = self.kre * self.K_loc + self.K_fr
        self.P_out                  = self.P_in - self.rho_ref * ( 0.5 * self.K * self.v_ref**2)  - self.rho_ref * (9.8 * self.length * math.cos(self.theta))
        self.T_out                  = self.T_ref
        self.mass_flow_rate_out     = self.mass_flow_rate_in



        
class grid:
    def __init__(self, name, type_name, thickness, grid_front_area, bundles_flow_area, grid_wetted_area, rods_wetted_at_grid_area, P_wet_at_grid, P_bundles, orientation):

        """
        Generate inherent property of grid.

        Keyword arguments:
        name                        -- the name of this component              ~
        type                        -- the type of this class                  ["grids_HELIOS"]
        thickness                   -- the thickness of the grid spacer        [m]
        grid_front_area             -- the front area of the grid              [m^2]
        bundles_flow_area           -- the diameter of the pipe                [m^2]
        grid_wetted_area            -- the wetted area of grid surface in grid [m^2]
        rods_wetted_at_grid_area    -- the wetted area of rods in grid         [m^2]
        orientation                 -- the orientation of the pipe             ["verical" / "horizontal"]
        P_wet_at_grid               -- the wetted perimeter of the grid        [m]
        P_bundles                   -- the wetted perimeter of the bundles     [m]

        """
        self.name                       = name
        self.type                       = type_name
        self.thickness                  = thickness
        self.length                     = self.thickness
        self.grid_front_area            = grid_front_area
        self.bundles_flow_area          = bundles_flow_area
        self.grid_wetted_area           = grid_wetted_area
        self.rods_wetted_at_grid_area   = rods_wetted_at_grid_area
        self.orientation                = orientation
        self.P_wet_at_grid              = P_wet_at_grid
        self.P_bundles                  = P_bundles


    def Theta(self):
        if self.orientation == "vertical":
            self.theta         = 0
        if self.orientation == "horizontal":
            self.theta         = math.pi / 2

    def calculation(self, inletcondition):
        self.Theta()
        self.T_in                   = inletcondition.T_out
        self.mass_flow_rate_in      = inletcondition.mass_flow_rate_out
        self.P_in                   = inletcondition.P_out
        self.T_ref                  = self.T_in
        self.P_ref                  = self.P_in
        self.mass_flow_rate         = self.mass_flow_rate_in
        self.rho_ref                = 11047 - 1.2564 * self.T_ref
        self.mu                     = 4.94e-4 * math.exp( 754.1 / self.T_ref )
        self.grid_flow_area         = self.bundles_flow_area - self.grid_front_area
        self.Dh_at_grid             = 4 * self.grid_flow_area / self.P_wet_at_grid
        self.Dh_at_bundles          = 4 * self.bundles_flow_area / self.P_bundles
        self.v_ref_at_bundles       = self.mass_flow_rate / ( self.rho_ref * self.bundles_flow_area )
        self.v_ref_at_grid          = self.mass_flow_rate / ( self.rho_ref * self.grid_flow_area )
        self.Re_at_grid             = self.v_ref_at_grid * self.Dh_at_grid * self.rho_ref / self.mu
        self.Re_at_bundles          = self.v_ref_at_bundles * self.Dh_at_bundles * self.rho_ref / self.mu
        self.mass_flux_at_grid      = self.mass_flow_rate / self.grid_flow_area
        # region term_grid_form
        self.C_grid_form            = 2.75 - 0.27 * math.log10( self.Re_at_bundles )
        self.epsilon                = self.grid_front_area / self.bundles_flow_area
        self.term_grid_form         = self.C_grid_form * self.epsilon / ( 1 - self.epsilon ) ** 2
        # endregion

        # region term_grid_fric

        if self.thickness - (3.e4 * self.mu) / self.mass_flux_at_grid >= 0:
            self.C_grid_fric_lam        = 1.328 * (self.mass_flux_at_grid * (self.thickness - (3.e4 * self.mu) / self.mass_flux_at_grid) /self.mu ) ** -0.5
            self.C_grid_fric_tur        = 0.523 * (math.log ( 0.06 * self.mass_flux_at_grid * ( self.thickness - (3.e4 * self.mu ) / self.mass_flux_at_grid ) / self.mu , math.e ) ) ** -2
            self.C_grid_fric            = self.C_grid_fric_lam * (3.e4 * self.mu)/ ( self.mass_flux_at_grid * self.thickness ) + self.C_grid_fric_tur * ( ( self.thickness - ( 3.e4 * self.mu )/ self.mass_flux_at_grid ) / self.thickness )

        else:
            self.C_grid_fric_lam        = 1.328 * (self.mass_flux_at_grid * self.thickness  /self.mu ) ** -0.5
            self.C_grid_fric            = self.C_grid_fric_lam * (1.e4 * self.mu)/ ( self.mass_flux_at_grid * self.thickness )

        self.term_grid_fric         = self.C_grid_fric * self.grid_wetted_area / self.bundles_flow_area * 1 / ( 1 - self.epsilon ) ** 2
        # endregion

        # region term_rod_fric
        self.C_rod_fric             = 0.184 * self.Re_at_grid ** (-0.2)
        self.term_rod_fric          = self.C_rod_fric * self.rods_wetted_at_grid_area / self.bundles_flow_area / ( 1 - self.epsilon )**2
        # endregion

        self.K                      = self.term_grid_form + self.term_grid_fric + self.term_rod_fric

        self.P_out                  = self.P_in - self.rho_ref * ( 0.5 * self.K * self.v_ref_at_bundles**2) - self.rho_ref * (9.8 * self.thickness * math.cos(self.theta))
        self.T_out                  = self.T_ref
        self.mass_flow_rate_out     = self.mass_flow_rate_in
        print "something, Re_in_grid, term_grid_fric, term_grid_form", self.thickness - (3e4 * self.mu) / self.mass_flux_at_grid, self.Re_at_grid, self.term_grid_fric, self.term_grid_form

class discharge_into_vessel:
    ## Reference page 663, I.E. IDELCHIK
    def __init__(self, name, type_name,h, D, alpha):

        """
        Generate inherent property of discharge into vessel.

        Keyword arguments:
        name              -- the name of this component                ~
        type              -- the type of this class                    ["discharge into vessel"]
        h                 -- distance from the outlet face to baffle   [m]
        D                 -- diameter of the tube                      [m]
        alpha             -- tube nozzle angle                         [degrees]
        """
        self.name              = name
        self.type              = type_name
        self.length            = 0
        self.h                 = h
        self.diameter          = D
        self.alpha             = alpha

    def k_discharge_into_vessel(self):
        hperDx = np.array([0.10,0.15,0.20,0.25,0.30,0.40,0.50,0.60,0.70,1.0])
        alphay = np.array([0.,15.,30.,45.,60.,90.])
        kvaluez = np.array([[-100000000,-100000000,-100000000,-100000000,-100000000,-100000000,1.37,1.20,1.11,1.00], [-100000000,-100000000,-100000000,1.50,1.06,0.72,0.61,0.59,0.58,0.58],[-100000000,-100000000,1.23,0.79,0.66,0.64,0.66,0.66,0.67,0.67],[-100000000,1.50,0.85,0.73,0.75,0.79,0.81,0.82,0.82,0.82],[-100000000,0.98,0.76,0.80,0.90,0.96,1.00,1.01,1.02,1.02],[1.50,0.72,0.74,0.83,0.89,0.94,0.96,0.98,1.00,1.00]])
        k_fun = interpolate.interp2d(hperDx, alphay, kvaluez, kind='linear')
        self.K  = float(k_fun(self.hperD,self.alpha))
        if self.K < 0.58:
            raise Exception('error: Discharge into a vessel pressure drop coefficient out of database range!')


    def calculation(self, inletcondition):

        self.T_in                   = inletcondition.T_out
        self.mass_flow_rate_in      = inletcondition.mass_flow_rate_out
        self.P_in                   = inletcondition.P_out
        self.T_ref                  = self.T_in
        self.P_ref                  = self.P_in
        self.mass_flow_rate         = self.mass_flow_rate_in
        self.rho_ref                = 11047 - 1.2564 * self.T_ref
        self.mu                     = 4.94e-4 * math.exp( 754.1 / self.T_ref )
        self.v_ref                  = self.mass_flow_rate / (self.rho_ref * math.pi * self.diameter ** 2 / 4)

        self.hperD = self.h / self.diameter
        self.k_discharge_into_vessel()

        self.P_out                  = self.P_in - self.rho_ref * ( 0.5 * self.K * self.v_ref**2)
        self.T_out                  = self.T_ref
        self.mass_flow_rate_out     = self.mass_flow_rate


class entrance_from_vessel_to_tube:
    ## Reference page 663, I.E. IDELCHIK

    def __init__(self, name, type_name, delta, b, D):
        """
        Generate inherent property of discharge into vessel.

        Keyword arguments:
        name              -- the name of this component                         ~
        type              -- the type of this class                            ["entrance from vessel to tube"]
        delta             -- thickness of the tube wall expanded into vessel   [m]
        b                 -- length of the tube expanded into vessel           [m]
        D                 -- diameter of the tueb                              [m]
        """
        self.name                   = name
        self.type                   = type_name
        self.length                 = 0
        self.delta                  = delta
        self.b                      = b
        self.diameter               = D

    def k_entrance_in_tube(self,bperD_in,deltaperD_in):
        bperDx         = np.array([0.,0.002,0.005,0.010,0.020,0.050,0.100,0.200,0.300,0.500])
        deltaperDy     = np.array([0.,0.004,0.008,0.012,0.016,0.020,0.024,0.030,0.040,0.050])
        kvaluez        = np.array([[0.50,0.57,0.63,0.68,0.73,0.80,0.86,0.92,0.97,1.00],
                          [0.50,0.54,0.58,0.63,0.67,0.74,0.80,0.86,0.90,0.94],
                          [0.50,0.53,0.55,0.58,0.62,0.68,0.74,0.81,0.85,0.88],
                          [0.50,0.52,0.53,0.55,0.58,0.63,0.68,0.75,0.79,0.83],
                          [0.50,0.51,0.51,0.53,0.55,0.58,0.64,0.70,0.74,0.77],
                          [0.50,0.51,0.51,0.52,0.53,0.55,0.60,0.66,0.69,0.72],
                          [0.50,0.50,0.50,0.51,0.52,0.53,0.58,0.62,0.65,0.68],
                          [0.50,0.50,0.50,0.52,0.52,0.52,0.54,0.57,0.59,0.61],
                          [0.50,0.50,0.50,0.51,0.51,0.51,0.51,0.52,0.52,0.54],
                          [0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50]])
        k_fun = interpolate.interp2d(bperDx, deltaperDy, kvaluez, kind='linear')
        self.K = float(k_fun(bperD_in,deltaperD_in))

    def calculation(self, inletcondition):

        self.T_in                   = inletcondition.T_out
        self.mass_flow_rate_in      = inletcondition.mass_flow_rate_out
        self.P_in                   = inletcondition.P_out
        self.T_ref                  = self.T_in
        self.P_ref                  = self.P_in
        self.mass_flow_rate         = self.mass_flow_rate_in
        self.rho_ref                = 11047 - 1.2564 * self.T_ref
        self.mu                     = 4.94e-4 * math.exp( 754.1 / self.T_ref )
        self.v_ref                  = self.mass_flow_rate / (self.rho_ref * math.pi * self.diameter ** 2 / 4)

        self.bperD                  = self.b / self.diameter
        self.deltaperD              = self.delta / self.diameter
        self.k_entrance_in_tube(self.bperD,self.deltaperD)

        self.P_out                  = self.P_in - self.rho_ref * ( 0.5 * self.K * self.v_ref**2)
        self.T_out                  = self.T_ref
        self.mass_flow_rate_out     = self.mass_flow_rate

class bundles:

    def __init__(self, name, type_name, length, barrel_diameter, barrel_type, array_type, rod_number, rod_diameter, pitch,
                 orientation):
        """
        Generate inherent property of discharge into vessel.

        Keyword arguments:
        name              -- the name of this component                 ~
        type              -- the type of this class                     ["entrance from vessel to tube"]
        length            -- the length of the rod bundles              [m]
        barrel_type       -- the type of the barrel                     ["square" / "round"]
        barrel_diamater   -- the barrel diameter                        [m]
        array_type        -- the array type                             ["square" / "triangular"]
        rod_diameter      -- rod diameter                               [m]
        pitch             -- pitch between the rods                     [m]
        orientation       -- the orientation of the bundles             ["vertical" / "horizontal"]
        rod_number        -- the number of the rods                     ~
        """
        self.name                   = name
        self.type                   = type_name
        self.length                 = length
        self.barrel_type            = barrel_type
        self.barrel_diameter        = barrel_diameter
        self.array_type             = array_type
        self.rod_diameter           = rod_diameter
        self.pitch                  = pitch
        self.orientation            = orientation
        self.rod_number             = rod_number

    def Theta(self):
        if self.orientation == "vertical":
            self.theta              = 0
        if self.orientation == "horizontal":
            self.theta              = math.pi / 2


    def calculation(self, inletcondition):
        self.Theta()
        self.T_in                   = inletcondition.T_out
        self.mass_flow_rate_in      = inletcondition.mass_flow_rate_out
        self.P_in                   = inletcondition.P_out
        self.T_ref                  = self.T_in
        self.P_ref                  = float(self.P_in)
        self.mass_flow_rate         = self.mass_flow_rate_in
        self.rho_ref                = 11047 - 1.2564 * self.T_ref
        self.mu                     = 4.94e-4 * math.exp( 754.1 / self.T_ref )
        if self.barrel_type is "round":
            self.wetperimeter       = (math.pi * self.barrel_diameter + self.rod_number * math.pi * self.rod_diameter)
            self.area               = (math.pi * (self.barrel_diameter / 2) ** 2 - self.rod_number * math.pi * (self.rod_diameter / 2)**2 )
            self.v_ref              = self.mass_flow_rate / (self.area * self.rho_ref)
            self.Dh                 = 4 * self.area / self.wetperimeter
            self.Re                 = self.v_ref * self.Dh * self.rho_ref / self.mu

        self.f                      = 0.316 * self.Re**(-0.25)
        self.P_out                  = self.P_in - self.rho_ref * ( 9.8 * self.length * math.cos(self.theta) + self.f * self.length / self.Dh * self.v_ref ** 2. / 2.)
        self.T_out                  = self.T_ref
        self.mass_flow_rate_out     = self.mass_flow_rate

class tee:
    def __init__(self, name, type_name, length, diameter, ratio_of_outlet_inlet_flow_rate, surfaceroughness, orientation):
        """
        Generate inherent property of tee.

        Keyword arguments:
        name                              -- the name of this component                 ~
        type                              -- the type of this class                     ["tee-straight" / "tee-elbow"]
        length                            -- the length of the rod bundles              [m]
        diameter                          -- diameter                                   [m]
        surfaceroughness                  -- surfaceroughness                           [m]
        ratio_of_outlet_inlet_flow_rate   -- outlet flow rate / inlet flow rate         [m]
        orientation                       -- the orientation of the bundles             ["vertical" / "horizontal"]
        """
        self.name                              = name
        self.type                              = type_name
        self.length                            = length
        self.diameter                          = diameter
        self.ratio_of_outlet_inlet_flow_rate   = ratio_of_outlet_inlet_flow_rate
        self.surfaceroughness                  = surfaceroughness
        self.orientation                       = orientation

    def theta(self):
        if self.orientation == "vertical":
            self.theta              = 0
        if self.orientation == "horizontal":
            self.theta              = math.pi / 2

    def fric_f_straight(self):
        if self.Re > 3000:
            self.f             = (1/( -2 * math.log10(self.surfaceroughness / ( 3.7 * self.diameter ) + 2.51 / self.Re * ( 1.14 - 2 * math.log10( math.fabs(self.surfaceroughness / self.diameter - 21.25 / self.Re**0.9 )) ) )))**2
        if self.Re < 2000:
            self.f             = 64 / self.Re
        if self.Re >= 2000 and self.Re <= 3000:
            self.f             = (3.75 - 8250 / self.Re) * ( ( 1 / ( -2 * math.log10(self.surfaceroughness / ( 3.7 * self.diameter ) + 2.51 / 3000 * ( 1.14 - 2 * math.log10( math.fabs(self.surfaceroughness / self.diameter - 21.25 / 3000**0.9 )) ) )))**2 - 64 / 2200 ) + 64 / 2200

    def form_k(self):
        ratio_of_outlet_inlet_flow_ratex = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        kvaluey = np.array([0.98, 0.87, 0.90, 0.98, 1.12, 1.29])
        k_fun = interpolate.interp1d(ratio_of_outlet_inlet_flow_ratex, kvaluey, kind='linear')
        self.K  = float( k_fun(self.ratio_of_outlet_inlet_flow_rate) )

    def calculation(self, inletcondition):
        self.theta()
        self.T_in              = inletcondition.T_out
        self.mass_flow_rate_in = inletcondition.mass_flow_rate_out
        self.P_in              = inletcondition.P_out

        self.T_ref             = self.T_in
        self.P_ref             = self.P_in
        self.mass_flow_rate    = self.mass_flow_rate_in

        self.rho_ref           = 11047-1.2564*self.T_ref
        self.mu                = 4.94e-4 * math.exp(754.1/self.T_ref)
        self.v_ref             = self.mass_flow_rate / ( self.rho_ref * math.pi * ( self.diameter / 2)**2 )
        self.Re                = self.ratio_of_outlet_inlet_flow_rate * self.mass_flow_rate * self.diameter / (math.pi * ( self.diameter / 2)**2 * self.mu)

        if self.type == "tee-straight":
            self.fric_f_straight()
            self.P_out         = self.P_in - self.rho_ref * ( 9.8 * self.length * math.cos(self.theta) + self.f*self.length / self.diameter * self.v_ref**2. / 2.)

        if self.type == "tee-elbow":
            self.form_k()
            self.P_out         = self.P_in - self.rho_ref * ( 9.8 * self.length * math.cos(self.theta) + 0.5 * self.K * self.v_ref**2)
        self.T_out                  = self.T_ref
        self.mass_flow_rate_out     = self.mass_flow_rate

