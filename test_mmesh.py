from vector3 import Vector3
from mesh import MeshPFV, MeshFacetPFV, MeshIV, MeshFacet
from mmesh import measure_mesh, face_pyramid_volume
from pytest import approx
import pytest

def print_facets(mesh):
	print('Beginning Mesh')
	for facet in mesh:
		print(f'  {facet.normal}')
		for vertex in facet:
			print(f'    {vertex}')

def test_tetrahedron_volume():
	regular_tetrahedron_face = MeshFacetPFV(
		[
			Vector3(1,0,0),
			Vector3(0,1,0),
			Vector3(0,0,1)
		],
		Vector3(0.57735026919,0.57735026919,0.57735026919)
	)
	regular_pyramid_face = MeshFacetPFV(
		[
			Vector3(1,-1,-1),
			Vector3(1,1,-1),
			Vector3(1,1,1),
			Vector3(1,-1,1)
		],
		Vector3(1,0,0)
	)
	assert 1/6 == approx(face_pyramid_volume(regular_tetrahedron_face), abs=0.0001)
	assert 4/3 == approx(face_pyramid_volume(regular_pyramid_face), abs=0.0001)

def test_mesh_volume_pfv():
	centered_cube_mesh = MeshPFV([
		MeshFacetPFV([Vector3(1,1,1), Vector3(-1,1,1), Vector3(1,-1,1)], Vector3(0,0,1)),
		MeshFacetPFV([Vector3(-1,-1,1), Vector3(-1,1,1), Vector3(1,-1,1)], Vector3(0,0,1)),

		MeshFacetPFV([Vector3(1,1,-1), Vector3(-1,1,-1), Vector3(1,-1,-1)], Vector3(0,0,-1)),
		MeshFacetPFV([Vector3(-1,-1,-1), Vector3(-1,1,-1), Vector3(1,-1,-1)], Vector3(0,0,-1)),
		
		MeshFacetPFV([Vector3(1,1,1), Vector3(-1,1,1), Vector3(1,1,-1)], Vector3(0,1,0)),
		MeshFacetPFV([Vector3(-1,1,-1), Vector3(-1,1,1), Vector3(1,1,-1)], Vector3(0,1,0)),
		
		MeshFacetPFV([Vector3(1,-1,1), Vector3(-1,-1,1), Vector3(1,-1,-1)], Vector3(0,-1,0)),
		MeshFacetPFV([Vector3(-1,-1,-1), Vector3(-1,-1,1), Vector3(1,-1,-1)], Vector3(0,-1,0)),
		
		MeshFacetPFV([Vector3(1,1,1), Vector3(1,-1,1), Vector3(1,1,-1)], Vector3(1,0,0)),
		MeshFacetPFV([Vector3(1,-1,-1), Vector3(1,-1,1), Vector3(1,1,-1)], Vector3(1,0,0)),
		
		MeshFacetPFV([Vector3(-1,1,1), Vector3(-1,-1,1), Vector3(-1,1,-1)], Vector3(-1,0,0)),
		MeshFacetPFV([Vector3(-1,-1,-1), Vector3(-1,-1,1), Vector3(-1,1,-1)], Vector3(-1,0,0)),
	])
	corner_cube_mesh = MeshPFV([
		MeshFacetPFV([Vector3(1,1,1), Vector3(1,0,1), Vector3(1,1,0)], Vector3(1,0,0)),
		MeshFacetPFV([Vector3(1,0,0), Vector3(1,1,0), Vector3(1,0,1)], Vector3(1,0,0)),
		
		MeshFacetPFV([Vector3(0,1,1), Vector3(0,1,0), Vector3(0,0,1)], Vector3(-1,0,0)),
		MeshFacetPFV([Vector3(0,0,0), Vector3(0,0,1), Vector3(0,1,0)], Vector3(-1,0,0)),

		MeshFacetPFV([Vector3(1,1,1), Vector3(1,1,0), Vector3(0,1,1)], Vector3(0,1,0)),
		MeshFacetPFV([Vector3(0,1,0), Vector3(0,1,1), Vector3(1,1,0)], Vector3(0,1,0)),
		
		MeshFacetPFV([Vector3(1,0,1), Vector3(0,0,1), Vector3(1,0,0)], Vector3(0,-1,0)),
		MeshFacetPFV([Vector3(0,0,0), Vector3(1,0,0), Vector3(0,0,1)], Vector3(0,-1,0)),

		MeshFacetPFV([Vector3(1,1,1), Vector3(0,1,1), Vector3(1,0,1)], Vector3(0,0,1)),
		MeshFacetPFV([Vector3(0,0,1), Vector3(1,0,1), Vector3(0,1,1)], Vector3(0,0,1)),

		MeshFacetPFV([Vector3(1,1,0), Vector3(1,0,0), Vector3(0,1,0)], Vector3(0,0,-1)),
		MeshFacetPFV([Vector3(0,0,0), Vector3(0,1,0), Vector3(1,0,0)], Vector3(0,0,-1)),
	])
	offset_cube_mesh = MeshPFV([
		MeshFacetPFV([Vector3(5,1,1), Vector3(3,1,1), Vector3(5,-1,1)], Vector3(0,0,1)),
		MeshFacetPFV([Vector3(3,-1,1), Vector3(3,1,1), Vector3(5,-1,1)], Vector3(0,0,1)),

		MeshFacetPFV([Vector3(5,1,-1), Vector3(3,1,-1), Vector3(5,-1,-1)], Vector3(0,0,-1)),
		MeshFacetPFV([Vector3(3,-1,-1), Vector3(3,1,-1), Vector3(5,-1,-1)], Vector3(0,0,-1)),
		
		MeshFacetPFV([Vector3(5,1,1), Vector3(3,1,1), Vector3(5,1,-1)], Vector3(0,1,0)),
		MeshFacetPFV([Vector3(3,1,-1), Vector3(3,1,1), Vector3(5,1,-1)], Vector3(0,1,0)),
		
		MeshFacetPFV([Vector3(5,-1,1), Vector3(3,-1,1), Vector3(5,-1,-1)], Vector3(0,-1,0)),
		MeshFacetPFV([Vector3(3,-1,-1), Vector3(3,-1,1), Vector3(5,-1,-1)], Vector3(0,-1,0)),
		
		MeshFacetPFV([Vector3(5,1,1), Vector3(5,-1,1), Vector3(5,1,-1)], Vector3(1,0,0)),
		MeshFacetPFV([Vector3(5,-1,-1), Vector3(5,-1,1), Vector3(5,1,-1)], Vector3(1,0,0)),
		
		MeshFacetPFV([Vector3(3,1,1), Vector3(3,-1,1), Vector3(3,1,-1)], Vector3(-1,0,0)),
		MeshFacetPFV([Vector3(3,-1,-1), Vector3(3,-1,1), Vector3(3,1,-1)], Vector3(-1,0,0)),
	])
	print('PFV Solids')
	print_facets(centered_cube_mesh)
	print_facets(corner_cube_mesh)
	print_facets(offset_cube_mesh)
	measure_mesh(centered_cube_mesh, volume=True, area=True, length=True)
	measure_mesh(corner_cube_mesh, volume=True, area=True, length=True)
	measure_mesh(offset_cube_mesh, volume=True, area=True, length=True)
	assert 8.0 == approx(centered_cube_mesh.meta['volume'], abs=0.0001)
	assert 8.0 == approx(offset_cube_mesh.meta['volume'], abs=0.0001)
	assert 1.0 == approx(corner_cube_mesh.meta['volume'], abs=0.0001)
	assert 24.0 == approx(centered_cube_mesh.meta['area'], abs=0.0001)
	assert 24.0 == approx(offset_cube_mesh.meta['area'], abs=0.0001)
	assert 6.0 == approx(corner_cube_mesh.meta['area'], abs=0.0001)
	assert 2.0 == approx(centered_cube_mesh.meta['x_length'], abs=0.0001)
	assert 2.0 == approx(offset_cube_mesh.meta['x_length'], abs=0.0001)
	assert 1.0 == approx(corner_cube_mesh.meta['x_length'], abs=0.0001)
	assert 2.0 == approx(centered_cube_mesh.meta['y_length'], abs=0.0001)
	assert 2.0 == approx(offset_cube_mesh.meta['y_length'], abs=0.0001)
	assert 1.0 == approx(corner_cube_mesh.meta['y_length'], abs=0.0001)
	assert 2.0 == approx(centered_cube_mesh.meta['z_length'], abs=0.0001)
	assert 2.0 == approx(offset_cube_mesh.meta['z_length'], abs=0.0001)
	assert 1.0 == approx(corner_cube_mesh.meta['z_length'], abs=0.0001)
def test_mesh_volume_iv():
	centered_cube_mesh = MeshIV([
		MeshFacet([Vector3(1,1,1), Vector3(-1,1,1), Vector3(1,-1,1)], Vector3(0,0,1)),
		MeshFacet([Vector3(-1,-1,1), Vector3(-1,1,1), Vector3(1,-1,1)], Vector3(0,0,1)),

		MeshFacet([Vector3(1,1,-1), Vector3(-1,1,-1), Vector3(1,-1,-1)], Vector3(0,0,-1)),
		MeshFacet([Vector3(-1,-1,-1), Vector3(-1,1,-1), Vector3(1,-1,-1)], Vector3(0,0,-1)),
		
		MeshFacet([Vector3(1,1,1), Vector3(-1,1,1), Vector3(1,1,-1)], Vector3(0,1,0)),
		MeshFacet([Vector3(-1,1,-1), Vector3(-1,1,1), Vector3(1,1,-1)], Vector3(0,1,0)),
		
		MeshFacet([Vector3(1,-1,1), Vector3(-1,-1,1), Vector3(1,-1,-1)], Vector3(0,-1,0)),
		MeshFacet([Vector3(-1,-1,-1), Vector3(-1,-1,1), Vector3(1,-1,-1)], Vector3(0,-1,0)),
		
		MeshFacet([Vector3(1,1,1), Vector3(1,-1,1), Vector3(1,1,-1)], Vector3(1,0,0)),
		MeshFacet([Vector3(1,-1,-1), Vector3(1,-1,1), Vector3(1,1,-1)], Vector3(1,0,0)),
		
		MeshFacet([Vector3(-1,1,1), Vector3(-1,-1,1), Vector3(-1,1,-1)], Vector3(-1,0,0)),
		MeshFacet([Vector3(-1,-1,-1), Vector3(-1,-1,1), Vector3(-1,1,-1)], Vector3(-1,0,0))
	])
	corner_cube_mesh = MeshIV([
		MeshFacet([Vector3(1,1,1), Vector3(1,0,1), Vector3(1,1,0)], Vector3(1,0,0)),
		MeshFacet([Vector3(1,0,0), Vector3(1,1,0), Vector3(1,0,1)], Vector3(1,0,0)),
		
		MeshFacet([Vector3(0,1,1), Vector3(0,1,0), Vector3(0,0,1)], Vector3(-1,0,0)),
		MeshFacet([Vector3(0,0,0), Vector3(0,0,1), Vector3(0,1,0)], Vector3(-1,0,0)),

		MeshFacet([Vector3(1,1,1), Vector3(1,1,0), Vector3(0,1,1)], Vector3(0,1,0)),
		MeshFacet([Vector3(0,1,0), Vector3(0,1,1), Vector3(1,1,0)], Vector3(0,1,0)),
		
		MeshFacet([Vector3(1,0,1), Vector3(0,0,1), Vector3(1,0,0)], Vector3(0,-1,0)),
		MeshFacet([Vector3(0,0,0), Vector3(1,0,0), Vector3(0,0,1)], Vector3(0,-1,0)),

		MeshFacet([Vector3(1,1,1), Vector3(0,1,1), Vector3(1,0,1)], Vector3(0,0,1)),
		MeshFacet([Vector3(0,0,1), Vector3(1,0,1), Vector3(0,1,1)], Vector3(0,0,1)),

		MeshFacet([Vector3(1,1,0), Vector3(1,0,0), Vector3(0,1,0)], Vector3(0,0,-1)),
		MeshFacet([Vector3(0,0,0), Vector3(0,1,0), Vector3(1,0,0)], Vector3(0,0,-1))
	])
	offset_cube_mesh = MeshIV([
		MeshFacet([Vector3(5,1,1), Vector3(3,1,1), Vector3(5,-1,1)], Vector3(0,0,1)),
		MeshFacet([Vector3(3,-1,1), Vector3(3,1,1), Vector3(5,-1,1)], Vector3(0,0,1)),

		MeshFacet([Vector3(5,1,-1), Vector3(3,1,-1), Vector3(5,-1,-1)], Vector3(0,0,-1)),
		MeshFacet([Vector3(3,-1,-1), Vector3(3,1,-1), Vector3(5,-1,-1)], Vector3(0,0,-1)),
		
		MeshFacet([Vector3(5,1,1), Vector3(3,1,1), Vector3(5,1,-1)], Vector3(0,1,0)),
		MeshFacet([Vector3(3,1,-1), Vector3(3,1,1), Vector3(5,1,-1)], Vector3(0,1,0)),
		
		MeshFacet([Vector3(5,-1,1), Vector3(3,-1,1), Vector3(5,-1,-1)], Vector3(0,-1,0)),
		MeshFacet([Vector3(3,-1,-1), Vector3(3,-1,1), Vector3(5,-1,-1)], Vector3(0,-1,0)),
		
		MeshFacet([Vector3(5,1,1), Vector3(5,-1,1), Vector3(5,1,-1)], Vector3(1,0,0)),
		MeshFacet([Vector3(5,-1,-1), Vector3(5,-1,1), Vector3(5,1,-1)], Vector3(1,0,0)),
		
		MeshFacet([Vector3(3,1,1), Vector3(3,-1,1), Vector3(3,1,-1)], Vector3(-1,0,0)),
		MeshFacet([Vector3(3,-1,-1), Vector3(3,-1,1), Vector3(3,1,-1)], Vector3(-1,0,0))
	])
	print('IV Solids')
	print_facets(centered_cube_mesh)
	print_facets(corner_cube_mesh)
	print_facets(offset_cube_mesh)
	measure_mesh(centered_cube_mesh, volume=True, area=True, length=True)
	measure_mesh(corner_cube_mesh, volume=True, area=True, length=True)
	measure_mesh(offset_cube_mesh, volume=True, area=True, length=True)
	assert 8.0 == approx(centered_cube_mesh.meta['volume'], abs=0.0001)
	assert 8.0 == approx(offset_cube_mesh.meta['volume'], abs=0.0001)
	assert 1.0 == approx(corner_cube_mesh.meta['volume'], abs=0.0001)
	assert 24.0 == approx(centered_cube_mesh.meta['area'], abs=0.0001)
	assert 24.0 == approx(offset_cube_mesh.meta['area'], abs=0.0001)
	assert 6.0 == approx(corner_cube_mesh.meta['area'], abs=0.0001)
	assert 2.0 == approx(centered_cube_mesh.meta['x_length'], abs=0.0001)
	assert 2.0 == approx(offset_cube_mesh.meta['x_length'], abs=0.0001)
	assert 1.0 == approx(corner_cube_mesh.meta['x_length'], abs=0.0001)
	assert 2.0 == approx(centered_cube_mesh.meta['y_length'], abs=0.0001)
	assert 2.0 == approx(offset_cube_mesh.meta['y_length'], abs=0.0001)
	assert 1.0 == approx(corner_cube_mesh.meta['y_length'], abs=0.0001)
	assert 2.0 == approx(centered_cube_mesh.meta['z_length'], abs=0.0001)
	assert 2.0 == approx(offset_cube_mesh.meta['z_length'], abs=0.0001)
	assert 1.0 == approx(corner_cube_mesh.meta['z_length'], abs=0.0001)

pytest.main(["-v", "--tb=line", "-rN", __file__])