import re
from struct import unpack, error as StructError
from vector3 import Vector3
from mesh import MeshFacetPFV, MeshPFV

def parse_exp(sign, mantissa, e_sign, exponent):
	return (-1 if sign == '-' else 1) * float(mantissa) * (10 ** ((-1 if e_sign == '-' else 1) * int(exponent)))

def parse_txt_stl(file_path):
	meta = {'format': 'stl', 'type': 'text'}
	facets = []
	try:
		with open(file_path, 'rt') as fp:
			ptn_solid = re.compile(r'\s*solid\s+(\S+)\s*')
			ptn_num_notation = re.compile(r'([+\-]?)(\d+(?:\.\d+)?)e([+\-]?)(\d+)')
			ptn_facet_normal = re.compile(r'\s*facet\s+normal\s+([+\-]?\d+(?:\.\d+)?e[+\-]?\d+)\s+([+\-]?\d+(?:\.\d+)?e[+\-]?\d+)\s+([+\-]?\d+(?:\.\d+)?e[+\-]?\d+)\s*')
			ptn_vertex = re.compile(r'\s*vertex\s+([+\-]?\d+(?:\.\d+)?e[+\-]?\d+)\s+([+\-]?\d+(?:\.\d+)?e[+\-]?\d+)\s+([+\-]?\d+(?:\.\d+)?e[+\-]?\d+)\s*')
			ptn_endfacet = re.compile(r'\s*endfacet\s*')

			current_face = None

			meta['name'] = ptn_solid.fullmatch(fp.readline()).group(1)
			
			for line in fp:
				if (match := ptn_facet_normal.fullmatch(line)) is not None:
					x = parse_exp(*ptn_num_notation.fullmatch(match.group(1)).group(1,2,3,4))
					y = parse_exp(*ptn_num_notation.fullmatch(match.group(2)).group(1,2,3,4))
					z = parse_exp(*ptn_num_notation.fullmatch(match.group(3)).group(1,2,3,4))
					normal = Vector3(x, y, z)
					current_face = {'vertices': [], 'normal': Vector3(0,0,0), 'given_normal': normal}
				elif (match := ptn_vertex.fullmatch(line)) is not None:
					x = parse_exp(*ptn_num_notation.fullmatch(match.group(1)).group(1,2,3,4))
					y = parse_exp(*ptn_num_notation.fullmatch(match.group(2)).group(1,2,3,4))
					z = parse_exp(*ptn_num_notation.fullmatch(match.group(3)).group(1,2,3,4))
					vertex = Vector3(x, y, z)
					current_face['vertices'].append(vertex)
				elif ptn_endfacet.fullmatch(line) is not None:
					current_face['normal'] = (current_face['vertices'][1] - current_face['vertices'][0]).cross(current_face['vertices'][2] - current_face['vertices'][0])
					if current_face['normal'].mag() > 0:
						current_face['normal'] = current_face['normal'].norm()
					facets.append(MeshFacetPFV(current_face['vertices'], current_face['normal'], data={'given_normal': current_face['given_normal']}))
				else:
					pass # Do nothing. Properly formatted STL files include both blank lines and extraneous semantic lines that can be safely ignored.
	except FileNotFoundError:
		raise FileNotFoundError(f'parse_txt_stl: Failed to locate file "{file_path}" in the current directory.')
	except AttributeError:
		raise AttributeError(f'parse_txt_stl: Failed parsing file "{file_path}". File may be malformed.')
	except IndexError:
		raise IndexError(f'parse_txt_stl: Failed parsing file "{file_path}". File may be malformed.')
	return MeshPFV(facets, meta)

def parse_bin_stl(file_path):
	meta = {'format': 'stl', 'type': 'binary'}
	facets = []

	try:
		with open(file_path, 'rb') as fp:
			meta['header'] = fp.read(80) # 80 byte header, generally ignored
			facet_count = unpack('<I', fp.read(4))[0] # 4-byte little-endian unsigned integer indicating the number of triangular facets
			for _ in range(facet_count):
				facet_bin = fp.read(50) # Each facet occupies exactly 50 bytes.
				if not facet_bin:
					raise EOFError(f'parse_bin_stl: Reached end-of-file before reading the provided number of facets in "{file_path}". File may be malformed.')
				ni, nj, nk, v1x, v1y, v1z, v2x, v2y, v2z, v3x, v3y, v3z, color = unpack('ffffffffffffH', facet_bin)
				given_normal = Vector3(ni, nj, nk)
				vector1 = Vector3(v1x, v1y, v1z)
				vector2 = Vector3(v2x, v2y, v2z)
				vector3 = Vector3(v3x, v3y, v3z)
				normal = (vector2 - vector1).cross(vector3 - vector1)
				if normal.mag() > 0:
					normal = normal.norm()
				facets.append(MeshFacetPFV([vector1, vector2, vector3], normal, data={'given_normal': given_normal,'color_data': color}))
	except FileNotFoundError:
		raise FileNotFoundError(f'parse_bin_stl: Failed to locate file "{file_path}" in the current directory.')
	except StructError:
		raise StructError(f'parse_bin_stl: Failed to unpack facet in "{file_path}". File may be malformed.')

	return MeshPFV(facets, meta)

def parse_stl(file_path):
	try:
		fp = open(file_path, 'rb')
		is_text = fp.read(5) == b'solid'
		fp.close()
	except FileNotFoundError:
		raise FileNotFoundError(f'parse_stl: Failed to locate file "{file_path}" in the current directory.')

	if is_text:
		return parse_txt_stl(file_path)
	else:
		return parse_bin_stl(file_path)