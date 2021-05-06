package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"time"

	"github.com/EliCDavis/mesh"
	"github.com/EliCDavis/vector"
)

var triTable = [][]uint8{{}, {0, 8, 3}, {0, 1, 9}, {1, 8, 3, 9, 8, 1}, {1, 2, 10}, {0, 8, 3, 1, 2, 10}, {9, 2, 10, 0, 2, 9}, {2, 8, 3, 2, 10, 8, 10, 9, 8}, {3, 11, 2}, {0, 11, 2, 8, 11, 0}, {1, 9, 0, 2, 3, 11}, {1, 11, 2, 1, 9, 11, 9, 8, 11}, {3, 10, 1, 11, 10, 3}, {0, 10, 1, 0, 8, 10, 8, 11, 10}, {3, 9, 0, 3, 11, 9, 11, 10, 9}, {9, 8, 10, 10, 8, 11}, {4, 7, 8}, {4, 3, 0, 7, 3, 4}, {0, 1, 9, 8, 4, 7}, {4, 1, 9, 4, 7, 1, 7, 3, 1}, {1, 2, 10, 8, 4, 7}, {3, 4, 7, 3, 0, 4, 1, 2, 10}, {9, 2, 10, 9, 0, 2, 8, 4, 7}, {2, 10, 9, 2, 9, 7, 2, 7, 3, 7, 9, 4}, {8, 4, 7, 3, 11, 2}, {11, 4, 7, 11, 2, 4, 2, 0, 4}, {9, 0, 1, 8, 4, 7, 2, 3, 11}, {4, 7, 11, 9, 4, 11, 9, 11, 2, 9, 2, 1}, {3, 10, 1, 3, 11, 10, 7, 8, 4}, {1, 11, 10, 1, 4, 11, 1, 0, 4, 7, 11, 4}, {4, 7, 8, 9, 0, 11, 9, 11, 10, 11, 0, 3}, {4, 7, 11, 4, 11, 9, 9, 11, 10}, {9, 5, 4}, {9, 5, 4, 0, 8, 3}, {0, 5, 4, 1, 5, 0}, {8, 5, 4, 8, 3, 5, 3, 1, 5}, {1, 2, 10, 9, 5, 4}, {3, 0, 8, 1, 2, 10, 4, 9, 5}, {5, 2, 10, 5, 4, 2, 4, 0, 2}, {2, 10, 5, 3, 2, 5, 3, 5, 4, 3, 4, 8}, {9, 5, 4, 2, 3, 11}, {0, 11, 2, 0, 8, 11, 4, 9, 5}, {0, 5, 4, 0, 1, 5, 2, 3, 11}, {2, 1, 5, 2, 5, 8, 2, 8, 11, 4, 8, 5}, {10, 3, 11, 10, 1, 3, 9, 5, 4}, {4, 9, 5, 0, 8, 1, 8, 10, 1, 8, 11, 10}, {5, 4, 0, 5, 0, 11, 5, 11, 10, 11, 0, 3}, {5, 4, 8, 5, 8, 10, 10, 8, 11}, {9, 7, 8, 5, 7, 9}, {9, 3, 0, 9, 5, 3, 5, 7, 3}, {0, 7, 8, 0, 1, 7, 1, 5, 7}, {1, 5, 3, 3, 5, 7}, {9, 7, 8, 9, 5, 7, 10, 1, 2}, {10, 1, 2, 9, 5, 0, 5, 3, 0, 5, 7, 3}, {8, 0, 2, 8, 2, 5, 8, 5, 7, 10, 5, 2}, {2, 10, 5, 2, 5, 3, 3, 5, 7}, {7, 9, 5, 7, 8, 9, 3, 11, 2}, {9, 5, 7, 9, 7, 2, 9, 2, 0, 2, 7, 11}, {2, 3, 11, 0, 1, 8, 1, 7, 8, 1, 5, 7}, {11, 2, 1, 11, 1, 7, 7, 1, 5}, {9, 5, 8, 8, 5, 7, 10, 1, 3, 10, 3, 11}, {5, 7, 0, 5, 0, 9, 7, 11, 0, 1, 0, 10, 11, 10, 0}, {11, 10, 0, 11, 0, 3, 10, 5, 0, 8, 0, 7, 5, 7, 0}, {11, 10, 5, 7, 11, 5}, {10, 6, 5}, {0, 8, 3, 5, 10, 6}, {9, 0, 1, 5, 10, 6}, {1, 8, 3, 1, 9, 8, 5, 10, 6}, {1, 6, 5, 2, 6, 1}, {1, 6, 5, 1, 2, 6, 3, 0, 8}, {9, 6, 5, 9, 0, 6, 0, 2, 6}, {5, 9, 8, 5, 8, 2, 5, 2, 6, 3, 2, 8}, {2, 3, 11, 10, 6, 5}, {11, 0, 8, 11, 2, 0, 10, 6, 5}, {0, 1, 9, 2, 3, 11, 5, 10, 6}, {5, 10, 6, 1, 9, 2, 9, 11, 2, 9, 8, 11}, {6, 3, 11, 6, 5, 3, 5, 1, 3}, {0, 8, 11, 0, 11, 5, 0, 5, 1, 5, 11, 6}, {3, 11, 6, 0, 3, 6, 0, 6, 5, 0, 5, 9}, {6, 5, 9, 6, 9, 11, 11, 9, 8}, {5, 10, 6, 4, 7, 8}, {4, 3, 0, 4, 7, 3, 6, 5, 10}, {1, 9, 0, 5, 10, 6, 8, 4, 7}, {10, 6, 5, 1, 9, 7, 1, 7, 3, 7, 9, 4}, {6, 1, 2, 6, 5, 1, 4, 7, 8}, {1, 2, 5, 5, 2, 6, 3, 0, 4, 3, 4, 7}, {8, 4, 7, 9, 0, 5, 0, 6, 5, 0, 2, 6}, {7, 3, 9, 7, 9, 4, 3, 2, 9, 5, 9, 6, 2, 6, 9}, {3, 11, 2, 7, 8, 4, 10, 6, 5}, {5, 10, 6, 4, 7, 2, 4, 2, 0, 2, 7, 11}, {0, 1, 9, 4, 7, 8, 2, 3, 11, 5, 10, 6}, {9, 2, 1, 9, 11, 2, 9, 4, 11, 7, 11, 4, 5, 10, 6}, {8, 4, 7, 3, 11, 5, 3, 5, 1, 5, 11, 6}, {5, 1, 11, 5, 11, 6, 1, 0, 11, 7, 11, 4, 0, 4, 11}, {0, 5, 9, 0, 6, 5, 0, 3, 6, 11, 6, 3, 8, 4, 7}, {6, 5, 9, 6, 9, 11, 4, 7, 9, 7, 11, 9}, {10, 4, 9, 6, 4, 10}, {4, 10, 6, 4, 9, 10, 0, 8, 3}, {10, 0, 1, 10, 6, 0, 6, 4, 0}, {8, 3, 1, 8, 1, 6, 8, 6, 4, 6, 1, 10}, {1, 4, 9, 1, 2, 4, 2, 6, 4}, {3, 0, 8, 1, 2, 9, 2, 4, 9, 2, 6, 4}, {0, 2, 4, 4, 2, 6}, {8, 3, 2, 8, 2, 4, 4, 2, 6}, {10, 4, 9, 10, 6, 4, 11, 2, 3}, {0, 8, 2, 2, 8, 11, 4, 9, 10, 4, 10, 6}, {3, 11, 2, 0, 1, 6, 0, 6, 4, 6, 1, 10}, {6, 4, 1, 6, 1, 10, 4, 8, 1, 2, 1, 11, 8, 11, 1}, {9, 6, 4, 9, 3, 6, 9, 1, 3, 11, 6, 3}, {8, 11, 1, 8, 1, 0, 11, 6, 1, 9, 1, 4, 6, 4, 1}, {3, 11, 6, 3, 6, 0, 0, 6, 4}, {6, 4, 8, 11, 6, 8}, {7, 10, 6, 7, 8, 10, 8, 9, 10}, {0, 7, 3, 0, 10, 7, 0, 9, 10, 6, 7, 10}, {10, 6, 7, 1, 10, 7, 1, 7, 8, 1, 8, 0}, {10, 6, 7, 10, 7, 1, 1, 7, 3}, {1, 2, 6, 1, 6, 8, 1, 8, 9, 8, 6, 7}, {2, 6, 9, 2, 9, 1, 6, 7, 9, 0, 9, 3, 7, 3, 9}, {7, 8, 0, 7, 0, 6, 6, 0, 2}, {7, 3, 2, 6, 7, 2}, {2, 3, 11, 10, 6, 8, 10, 8, 9, 8, 6, 7}, {2, 0, 7, 2, 7, 11, 0, 9, 7, 6, 7, 10, 9, 10, 7}, {1, 8, 0, 1, 7, 8, 1, 10, 7, 6, 7, 10, 2, 3, 11}, {11, 2, 1, 11, 1, 7, 10, 6, 1, 6, 7, 1}, {8, 9, 6, 8, 6, 7, 9, 1, 6, 11, 6, 3, 1, 3, 6}, {0, 9, 1, 11, 6, 7}, {7, 8, 0, 7, 0, 6, 3, 11, 0, 11, 6, 0}, {7, 11, 6}, {7, 6, 11}, {3, 0, 8, 11, 7, 6}, {0, 1, 9, 11, 7, 6}, {8, 1, 9, 8, 3, 1, 11, 7, 6}, {10, 1, 2, 6, 11, 7}, {1, 2, 10, 3, 0, 8, 6, 11, 7}, {2, 9, 0, 2, 10, 9, 6, 11, 7}, {6, 11, 7, 2, 10, 3, 10, 8, 3, 10, 9, 8}, {7, 2, 3, 6, 2, 7}, {7, 0, 8, 7, 6, 0, 6, 2, 0}, {2, 7, 6, 2, 3, 7, 0, 1, 9}, {1, 6, 2, 1, 8, 6, 1, 9, 8, 8, 7, 6}, {10, 7, 6, 10, 1, 7, 1, 3, 7}, {10, 7, 6, 1, 7, 10, 1, 8, 7, 1, 0, 8}, {0, 3, 7, 0, 7, 10, 0, 10, 9, 6, 10, 7}, {7, 6, 10, 7, 10, 8, 8, 10, 9}, {6, 8, 4, 11, 8, 6}, {3, 6, 11, 3, 0, 6, 0, 4, 6}, {8, 6, 11, 8, 4, 6, 9, 0, 1}, {9, 4, 6, 9, 6, 3, 9, 3, 1, 11, 3, 6}, {6, 8, 4, 6, 11, 8, 2, 10, 1}, {1, 2, 10, 3, 0, 11, 0, 6, 11, 0, 4, 6}, {4, 11, 8, 4, 6, 11, 0, 2, 9, 2, 10, 9}, {10, 9, 3, 10, 3, 2, 9, 4, 3, 11, 3, 6, 4, 6, 3}, {8, 2, 3, 8, 4, 2, 4, 6, 2}, {0, 4, 2, 4, 6, 2}, {1, 9, 0, 2, 3, 4, 2, 4, 6, 4, 3, 8}, {1, 9, 4, 1, 4, 2, 2, 4, 6}, {8, 1, 3, 8, 6, 1, 8, 4, 6, 6, 10, 1}, {10, 1, 0, 10, 0, 6, 6, 0, 4}, {4, 6, 3, 4, 3, 8, 6, 10, 3, 0, 3, 9, 10, 9, 3}, {10, 9, 4, 6, 10, 4}, {4, 9, 5, 7, 6, 11}, {0, 8, 3, 4, 9, 5, 11, 7, 6}, {5, 0, 1, 5, 4, 0, 7, 6, 11}, {11, 7, 6, 8, 3, 4, 3, 5, 4, 3, 1, 5}, {9, 5, 4, 10, 1, 2, 7, 6, 11}, {6, 11, 7, 1, 2, 10, 0, 8, 3, 4, 9, 5}, {7, 6, 11, 5, 4, 10, 4, 2, 10, 4, 0, 2}, {3, 4, 8, 3, 5, 4, 3, 2, 5, 10, 5, 2, 11, 7, 6}, {7, 2, 3, 7, 6, 2, 5, 4, 9}, {9, 5, 4, 0, 8, 6, 0, 6, 2, 6, 8, 7}, {3, 6, 2, 3, 7, 6, 1, 5, 0, 5, 4, 0}, {6, 2, 8, 6, 8, 7, 2, 1, 8, 4, 8, 5, 1, 5, 8}, {9, 5, 4, 10, 1, 6, 1, 7, 6, 1, 3, 7}, {1, 6, 10, 1, 7, 6, 1, 0, 7, 8, 7, 0, 9, 5, 4}, {4, 0, 10, 4, 10, 5, 0, 3, 10, 6, 10, 7, 3, 7, 10}, {7, 6, 10, 7, 10, 8, 5, 4, 10, 4, 8, 10}, {6, 9, 5, 6, 11, 9, 11, 8, 9}, {3, 6, 11, 0, 6, 3, 0, 5, 6, 0, 9, 5}, {0, 11, 8, 0, 5, 11, 0, 1, 5, 5, 6, 11}, {6, 11, 3, 6, 3, 5, 5, 3, 1}, {1, 2, 10, 9, 5, 11, 9, 11, 8, 11, 5, 6}, {0, 11, 3, 0, 6, 11, 0, 9, 6, 5, 6, 9, 1, 2, 10}, {11, 8, 5, 11, 5, 6, 8, 0, 5, 10, 5, 2, 0, 2, 5}, {6, 11, 3, 6, 3, 5, 2, 10, 3, 10, 5, 3}, {5, 8, 9, 5, 2, 8, 5, 6, 2, 3, 8, 2}, {9, 5, 6, 9, 6, 0, 0, 6, 2}, {1, 5, 8, 1, 8, 0, 5, 6, 8, 3, 8, 2, 6, 2, 8}, {1, 5, 6, 2, 1, 6}, {1, 3, 6, 1, 6, 10, 3, 8, 6, 5, 6, 9, 8, 9, 6}, {10, 1, 0, 10, 0, 6, 9, 5, 0, 5, 6, 0}, {0, 3, 8, 5, 6, 10}, {10, 5, 6}, {11, 5, 10, 7, 5, 11}, {11, 5, 10, 11, 7, 5, 8, 3, 0}, {5, 11, 7, 5, 10, 11, 1, 9, 0}, {10, 7, 5, 10, 11, 7, 9, 8, 1, 8, 3, 1}, {11, 1, 2, 11, 7, 1, 7, 5, 1}, {0, 8, 3, 1, 2, 7, 1, 7, 5, 7, 2, 11}, {9, 7, 5, 9, 2, 7, 9, 0, 2, 2, 11, 7}, {7, 5, 2, 7, 2, 11, 5, 9, 2, 3, 2, 8, 9, 8, 2}, {2, 5, 10, 2, 3, 5, 3, 7, 5}, {8, 2, 0, 8, 5, 2, 8, 7, 5, 10, 2, 5}, {9, 0, 1, 5, 10, 3, 5, 3, 7, 3, 10, 2}, {9, 8, 2, 9, 2, 1, 8, 7, 2, 10, 2, 5, 7, 5, 2}, {1, 3, 5, 3, 7, 5}, {0, 8, 7, 0, 7, 1, 1, 7, 5}, {9, 0, 3, 9, 3, 5, 5, 3, 7}, {9, 8, 7, 5, 9, 7}, {5, 8, 4, 5, 10, 8, 10, 11, 8}, {5, 0, 4, 5, 11, 0, 5, 10, 11, 11, 3, 0}, {0, 1, 9, 8, 4, 10, 8, 10, 11, 10, 4, 5}, {10, 11, 4, 10, 4, 5, 11, 3, 4, 9, 4, 1, 3, 1, 4}, {2, 5, 1, 2, 8, 5, 2, 11, 8, 4, 5, 8}, {0, 4, 11, 0, 11, 3, 4, 5, 11, 2, 11, 1, 5, 1, 11}, {0, 2, 5, 0, 5, 9, 2, 11, 5, 4, 5, 8, 11, 8, 5}, {9, 4, 5, 2, 11, 3}, {2, 5, 10, 3, 5, 2, 3, 4, 5, 3, 8, 4}, {5, 10, 2, 5, 2, 4, 4, 2, 0}, {3, 10, 2, 3, 5, 10, 3, 8, 5, 4, 5, 8, 0, 1, 9}, {5, 10, 2, 5, 2, 4, 1, 9, 2, 9, 4, 2}, {8, 4, 5, 8, 5, 3, 3, 5, 1}, {0, 4, 5, 1, 0, 5}, {8, 4, 5, 8, 5, 3, 9, 0, 5, 0, 3, 5}, {9, 4, 5}, {4, 11, 7, 4, 9, 11, 9, 10, 11}, {0, 8, 3, 4, 9, 7, 9, 11, 7, 9, 10, 11}, {1, 10, 11, 1, 11, 4, 1, 4, 0, 7, 4, 11}, {3, 1, 4, 3, 4, 8, 1, 10, 4, 7, 4, 11, 10, 11, 4}, {4, 11, 7, 9, 11, 4, 9, 2, 11, 9, 1, 2}, {9, 7, 4, 9, 11, 7, 9, 1, 11, 2, 11, 1, 0, 8, 3}, {11, 7, 4, 11, 4, 2, 2, 4, 0}, {11, 7, 4, 11, 4, 2, 8, 3, 4, 3, 2, 4}, {2, 9, 10, 2, 7, 9, 2, 3, 7, 7, 4, 9}, {9, 10, 7, 9, 7, 4, 10, 2, 7, 8, 7, 0, 2, 0, 7}, {3, 7, 10, 3, 10, 2, 7, 4, 10, 1, 10, 0, 4, 0, 10}, {1, 10, 2, 8, 7, 4}, {4, 9, 1, 4, 1, 7, 7, 1, 3}, {4, 9, 1, 4, 1, 7, 0, 8, 1, 8, 7, 1}, {4, 0, 3, 7, 4, 3}, {4, 8, 7}, {9, 10, 8, 10, 11, 8}, {3, 0, 9, 3, 9, 11, 11, 9, 10}, {0, 1, 10, 0, 10, 8, 8, 10, 11}, {3, 1, 10, 11, 3, 10}, {1, 2, 11, 1, 11, 9, 9, 11, 8}, {3, 0, 9, 3, 9, 11, 1, 2, 9, 2, 11, 9}, {0, 2, 11, 8, 0, 11}, {3, 2, 11}, {2, 3, 8, 2, 8, 10, 10, 8, 9}, {9, 10, 2, 0, 9, 2}, {2, 3, 8, 2, 8, 10, 0, 1, 8, 1, 10, 8}, {1, 10, 2}, {1, 3, 8, 9, 1, 8}, {0, 9, 1}, {0, 3, 8}, {}}

var cornersFromEdge = [][]uint8{{0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3}, {1, 2, 3, 0, 5, 6, 7, 4, 4, 5, 6, 7}}

var surfaceLevel float64 = 0.5

var res uint = 512

var doSmoothing bool = false

var numThreads uint = 16

var chans []chan []mesh.Polygon

var f func(vector.Vector3) float64 = sphere_func

//var hashmap map[[3]float64]float64 = make(map[[3]float64]float64)

func sphere_func(v vector.Vector3) float64 {
	return 1.0 * math.Sqrt(math.Pow((v.X()-0.5), 2.0)+math.Pow((v.Y()-0.5), 2.0)+math.Pow((v.Z()-0.5), 2.0))
}

/*
func hash(v vector.Vector3) [3]float64 {
	result := [3]float64{v.X(), v.Y(), v.Z()}
	return result
}
*/
func evaluate(f func(vector.Vector3) float64, v vector.Vector3) float64 {
	//h := hash(v)
	//val, exists := hashmap[h]
	//if exists {
	//	return val
	//}
	val := f(v)
	//hashmap[h] = val
	return val
}

func mean(v1 vector.Vector3, v2 vector.Vector3, interpolate bool, f func(vector.Vector3) float64) vector.Vector3 {
	weight1 := 1.0
	weight2 := 1.0
	if interpolate {
		weight2 = (surfaceLevel - evaluate(f, v1)) / (evaluate(f, v2) - evaluate(f, v1))
		weight1 = 1.0 - weight2
	}
	result := ((v1.MultByConstant(weight1)).Add(v2.MultByConstant(weight2))).DivByConstant(weight1 + weight2)
	return result
}

func get_corners(x float64, y float64, z float64, dx float64, dy float64, dz float64) [8]vector.Vector3 {
	var result [8]vector.Vector3
	result[0] = vector.NewVector3(x, y, z)
	result[1] = vector.NewVector3(x+dx, y, z)
	result[2] = vector.NewVector3(x+dx, y, z+dz)
	result[3] = vector.NewVector3(x, y, z+dz)
	result[4] = vector.NewVector3(x, y+dy, z)
	result[5] = vector.NewVector3(x+dx, y+dy, z)
	result[6] = vector.NewVector3(x+dx, y+dy, z+dz)
	result[7] = vector.NewVector3(x, y+dy, z+dz)
	return result
}

func cube(f func(vector.Vector3) float64, gridNum uint, x_min float64, y_min float64, z_min float64, dx float64, dy float64, dz float64) ([5]mesh.Polygon, int) {
	i := gridNum % res
	j := (gridNum / res) % res
	k := gridNum / (res * res)
	x := x_min + (float64(i) * dx)
	y := y_min + (float64(j) * dy)
	z := z_min + (float64(k) * dz)

	var corners [8]vector.Vector3 = get_corners(x, y, z, dx, dy, dz)

	var cubeIndex uint = 0

	for cornerNum := uint(0); cornerNum < uint(len(corners)); cornerNum++ {
		if evaluate(f, corners[cornerNum]) < surfaceLevel {
			cubeIndex |= 1 << cornerNum
		}
	}
	triangulation := triTable[cubeIndex]
	var output [5]mesh.Polygon
	numFaces := len(triangulation) / 3
	for faceNum := 0; faceNum < numFaces; faceNum++ {
		var points [3]vector.Vector3
		for vertexNum := 0; vertexNum < 3; vertexNum++ {
			edgeIndex := triangulation[(faceNum*3)+vertexNum]
			indexA := cornersFromEdge[0][edgeIndex]
			indexB := cornersFromEdge[1][edgeIndex]
			points[vertexNum] = mean(corners[indexA], corners[indexB], doSmoothing, f)
		}
		poly, _ := mesh.NewPolygon(points[:], points[:])
		output[faceNum] = poly
	}
	return output, numFaces
}

func thread(f func(vector.Vector3) float64, threadNum uint, x_min float64, y_min float64, z_min float64, dx float64, dy float64, dz float64) {
	var allPolygons []mesh.Polygon

	numVertices := res * res * res
	gridNumStart := (numVertices / numThreads) * threadNum
	gridNumEnd := (numVertices / numThreads) * (threadNum + 1)
	if gridNumEnd > numVertices {
		gridNumEnd = numVertices
	}

	for gridNum := gridNumStart; gridNum < gridNumEnd; gridNum++ {
		polygons, numFaces := cube(f, gridNum, x_min, y_min, z_min, dx, dy, dz)
		allPolygons = append(allPolygons, polygons[:numFaces]...)
	}

	chans[threadNum] <- allPolygons
}

func march(f func(vector.Vector3) float64, x_min float64, x_max float64, y_min float64, y_max float64, z_min float64, z_max float64) (mesh.Model, error) {
	dx := (x_max - x_min) / float64(res)
	dy := (y_max - y_min) / float64(res)
	dz := (z_max - z_min) / float64(res)

	if numThreads > res*res*res {
		numThreads = res * res * res
	}

	chans = make([]chan []mesh.Polygon, numThreads)

	for threadNum := uint(0); threadNum < numThreads; threadNum++ {
		chans[threadNum] = make(chan []mesh.Polygon)
		go thread(f, threadNum, x_min, y_min, z_min, dx, dy, dz)
	}

	var allPolygons []mesh.Polygon

	for threadNum := uint(0); threadNum < numThreads; threadNum++ {
		polygons := <-chans[threadNum]
		allPolygons = append(allPolygons, polygons...)
	}

	return mesh.NewModel(allPolygons)
}

func main() {
	start := time.Now()
	model, err := march(f, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0)
	duration := time.Since(start)

	fmt.Println(duration)
	fmt.Println(duration.Nanoseconds())

	if err != nil {
		panic(err)
	}

	f, err := os.Create("out.obj")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	w := bufio.NewWriter(f)
	err = model.Save(w)
	if err != nil {
		panic(err)
	}

	w.Flush()
}
