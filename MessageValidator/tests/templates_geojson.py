#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Antonio Vaccarino'
__docformat__ = 'restructuredtext en' 

test_point = { "type": u"Point", "coordinates": [100.0, 0.0] }


test_linestring = { "type": u"LineString",
  "coordinates": [ [100.0, 0.0], [101.0, 1.0] ]
  }

test_polygon = { "type": u"Polygon",
  "coordinates": [
    [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ]
    ]
 }

test_polygon_b = { "type": "Polygon",
	  "coordinates": [
		  [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ],
		  [ [100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2] ]
	  ]
}

test_multipoint = { "type": "MultiPoint",
	  "coordinates": [ [100.0, 0.0], [101.0, 1.0] ]
}


test_multilinestring  = { "type": u"MultiLineString",
	  "coordinates": [
		  [ [100.0, 0.0], [101.0, 1.0] ],
		  [ [102.0, 2.0], [103.0, 3.0] ]
	  ]
}

test_multipolygon = { "type": u"MultiPolygon",
	  "coordinates": [
		  [[[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]]],
		  [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
			  [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]]]
	  ]
}

test_geometrycollection = { "type": u"GeometryCollection",
	  "geometries": [
			  { "type": u"Point",
				"coordinates": [100.0, 0.0]
		  },
			  { "type": u"LineString",
				"coordinates": [ [101.0, 0.0], [102.0, 1.0] ]
		  }
	  ]
}

test_feature = {
	"type": u"Feature",
	"geometry": {
		"type": u"LineString",
		"coordinates": [
			[100.0, 0.0], [101.0, 1.0]
		]
	},
	"properties": {
		"prop0": u"value0",
		"prop1": u"value1"
	}
}

test_feature_b = {
	"type": u"Feature",
	"geometry": {
		"type": u"GeometryCollection",
		"geometries": [
				{
				"type": u"Point",
				"coordinates": [100.0, 0.0]
			},
				{
				"type": u"LineString",
				"coordinates": [
					[101.0, 0.0], [102.0, 1.0]
				]
			}
		]
	},
	"properties": {
		"prop0": u"value0",
		"prop1": u"value1"
	}
}

test_featurecollection = {
	"type": u"FeatureCollection",
	"features": [
			{
			"type": u"Feature",
			"id": u"id0",
			"geometry": {
				"type": u"LineString",
				"coordinates": [
					[102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]
				]
			},
			"properties": {
				"prop0": u"value0",
				"prop1": u"value1"
			}
		},
			{
			"type": u"Feature",
			"id": u"id1",
			"geometry": {
				"type": u"Polygon",
				"coordinates": [
					[
						[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]
					]
				]
			},
			"properties": {
				"prop0": u"value0",
				"prop1": u"value1"
			}
		}
	]
}

test_featurecollection_b = {
	"type": u"FeatureCollection",
	"crs": {
		"type": u"name",
		"properties": {
			"name": u"EPSG",
			"code": 4326,
			"coordinate_order": [1, 0]
		}
	},
	"features": [
			{
			"type": u"Feature",
			"id": u"id0",
			"geometry": {
				"type": u"LineString",
				"coordinates": [
					[102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]
				]
			},
			"properties": {
				"prop0": u"value0",
				"prop1": u"value1"
			}
		},
			{
			"type": u"Feature",
			"id": u"id1",
			"geometry": {
				"type": u"Polygon",
				"coordinates": [
					[
						[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]
					]
				]
			},
			"properties": {
				"prop0": u"value0",
				"prop1": u"value1"
			}
		}
	]
}

test_feature_c = {
	"type": u"Feature",
	"geometry": {
		"type": u"LineString",
		"coordinates": [
			[100.0, 0.0], [101.0, 1.0]
		]
	},
	"properties": {
		"prop0": u"value0",
		"prop1": u"value1"
	},
	"foo": "bar"
}

test_feature_d = {
	"@namespaces":  {"":u"http://geojson.org/ns#"},
	"type": u"Feature",
	"geometry": {
		"type": u"LineString",
		"coordinates": [
			[100.0, 0.0], [101.0, 1.0]
		]
	},
	"properties": {
		"prop0": u"value0",
		"prop1": u"value1"
	}
}

test_feature_e = {
	"@namespaces":  {"":u"http://geojson.org/ns#", "atom":u"http://www.w3.org/2005/Atom"},
	"@type": u"atom:item",
	"type": u"Feature",
	"geometry": {
		"type": u"LineString",
		"coordinates": [
			[100.0, 0.0], [101.0, 1.0]
		]
	},
	"properties": {
		"atom:summary": u"Some GeoJSON Content",
		"atom:description": u"This content is also valid GeoJDIL."
	}
}

test_polygon_c = {
	"bbox": [-180.0, -90.0, 180.0, 90.0],
	"type": u"Polygon",
	"coordinates": [
		[ [-180.0, 10.0], [20.0, 90.0], [180.0, -5.0], [-30.0, -90.0], [-180.0, 10.0] ]
	]
}

test_featurecollection_c = {
	"type": u"FeatureCollection",
	"bbox": [100.0, 0.0, 105.0, 1.0],
	"features": [
			{
			"type": u"Feature",
			"id": u"id0",
			"bbox": [102.0, 0.0, 105.0, 1.0],
			"geometry": {
				"type": u"LineString",
				"coordinates": [
					[102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]
				]
			},
			"properties": {
				"prop0": u"value0",
				"prop1": u"value1"
			}
		},
			{
			"type": u"Feature",
			"id": u"id1",
			"bbox": [100.0, 0.0, 101.0, 1.0],
			"geometry": {
				"type": u"Polygon",
				"coordinates": [
					[
						[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]
					]
				]
			},
			"properties": {
				"prop0": u"value0",
				"prop1": u"value1"
			}
		}
	]
}

test_prevalidated_featurecollection = {
		"type": u"FeatureCollection",
		"features": [
				{ "type": u"Feature", "id": 0, "properties": { u"id": 1 }, "geometry": { "type": u"Polygon", "coordinates": [ [ [ 11.325308, 44.501608 ], [ 11.347063, 44.507618 ], [ 11.355957, 44.516752 ], [ 11.355957, 44.516752 ], [ 11.362327, 44.487666 ], [ 11.320621, 44.465792 ], [ 11.287448, 44.489349 ], [ 11.300429, 44.512906 ], [ 11.325308, 44.501608 ] ], [ [ 11.342255, 44.501728 ], [ 11.326871, 44.493315 ], [ 11.329996, 44.483820 ], [ 11.350668, 44.483820 ], [ 11.350668, 44.483820 ], [ 11.351750, 44.501488 ], [ 11.342255, 44.501728 ] ], [ [ 11.306679, 44.501248 ], [ 11.297184, 44.496079 ], [ 11.307039, 44.485262 ], [ 11.318818, 44.492474 ], [ 11.306679, 44.501248 ] ] ] } }

		]
	}


test_prevalidated_featurecollection_b = {
	"type": "FeatureCollection",
	"features": [
			{ "type": "Feature", "id": 0, "properties": { "id": 1 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 11.363207, 44.506289 ], [ 11.355957, 44.508820 ], [ 11.352708, 44.511857 ], [ 11.360283, 44.519637 ], [ 11.363207, 44.506289 ] ] ] } }
		,
			{ "type": "Feature", "id": 1, "properties": { "id": 1 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 11.348261, 44.508732 ], [ 11.351510, 44.505695 ], [ 11.358760, 44.503164 ], [ 11.362207, 44.487426 ], [ 11.320501, 44.465551 ], [ 11.287328, 44.489108 ], [ 11.300309, 44.512666 ], [ 11.325188, 44.501368 ], [ 11.346942, 44.507377 ], [ 11.348261, 44.508732 ] ], [ [ 11.342135, 44.501488 ], [ 11.326751, 44.493075 ], [ 11.329875, 44.483580 ], [ 11.350548, 44.483580 ], [ 11.351630, 44.501248 ], [ 11.342135, 44.501488 ] ], [ [ 11.306559, 44.501007 ], [ 11.297064, 44.495839 ], [ 11.306919, 44.485022 ], [ 11.318698, 44.492233 ], [ 11.306559, 44.501007 ] ], [ [ 11.317616, 44.484301 ], [ 11.314732, 44.476368 ], [ 11.325909, 44.476849 ], [ 11.317616, 44.484301 ] ] ] } }

	]
}

test_prevalidated_featurecollection_c = {
	"type": "FeatureCollection",
	"features": [
			{ "type": "Feature", "id": 0, "properties": { "id": 1 }, "geometry": { "type": "MultiPolygon", "coordinates": [ [ [ [ 11.348261, 44.508732 ], [ 11.351510, 44.505695 ], [ 11.358760, 44.503164 ], [ 11.362207, 44.487426 ], [ 11.320501, 44.465551 ], [ 11.287328, 44.489108 ], [ 11.300309, 44.512666 ], [ 11.325188, 44.501368 ], [ 11.346942, 44.507377 ], [ 11.348261, 44.508732 ] ], [ [ 11.342135, 44.501488 ], [ 11.326751, 44.493075 ], [ 11.329875, 44.483580 ], [ 11.350548, 44.483580 ], [ 11.351630, 44.501248 ], [ 11.342135, 44.501488 ] ], [ [ 11.306559, 44.501007 ], [ 11.297064, 44.495839 ], [ 11.306919, 44.485022 ], [ 11.318698, 44.492233 ], [ 11.306559, 44.501007 ] ], [ [ 11.317616, 44.484301 ], [ 11.314732, 44.476368 ], [ 11.325909, 44.476849 ], [ 11.317616, 44.484301 ] ] ], [ [ [ 11.337087, 44.509060 ], [ 11.325428, 44.505214 ], [ 11.310164, 44.511704 ], [ 11.323866, 44.517954 ], [ 11.337087, 44.509060 ] ] ], [ [ [ 11.306799, 44.498964 ], [ 11.312688, 44.493916 ], [ 11.300910, 44.494998 ], [ 11.301390, 44.495839 ], [ 11.306799, 44.498964 ] ] ], [ [ [ 11.332880, 44.493315 ], [ 11.341894, 44.499565 ], [ 11.341894, 44.499565 ], [ 11.349587, 44.500406 ], [ 11.347423, 44.493075 ], [ 11.332880, 44.493315 ] ] ] ] } }

	]
}