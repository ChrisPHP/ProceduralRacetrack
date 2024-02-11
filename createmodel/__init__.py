import pyvista as pv

class CreateModel:
    
    def create_mesh_line(self, points):
        mesh = pv.PolyData
        for i in range(len(points)-1):
            tube = pv.Tube(points[i], points[i+1], 1, 1, 6)
            mesh = mesh.append_polydata(tube)
        mesh.save('racetrack.ply')