package main

/*
import (
	"bufio"
	"math"
	"os"

	"github.com/EliCDavis/mesh"
	"github.com/EliCDavis/vector"
)

// MakeShape creates a shape at 0, 0, 0 with a certain number of sides with
// each point of the shape a distance from 0, 0, 0 equal to the radius
// passed in.
func MakeShape(sides int, radius float64) (mesh.Model, error) {
	polys := make([]mesh.Polygon, sides)

	angleIncrement := (1.0 / float64(sides)) * 2.0 * math.Pi
	for sideIndex := 0; sideIndex < sides; sideIndex++ {
		angle := angleIncrement * float64(sideIndex)
		angleNext := angleIncrement * (float64(sideIndex) + 1)

		points := []vector.Vector3{
			vector.NewVector3(0, 0, 0),
			vector.NewVector3(math.Cos(angleNext)*radius, 1, math.Sin(angleNext)*radius),
			vector.NewVector3(math.Cos(angle)*radius, 0, math.Sin(angle)*radius),
		}

		poly, _ := mesh.NewPolygon(points, points)

		polys[sideIndex] = poly
	}

	return mesh.NewModel(polys)
}

func main2() {
	shape, err := MakeShape(10, 5.0)
	if err != nil {
		panic(err)
	}

	f, err := os.Create("out.obj")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	w := bufio.NewWriter(f)
	err = shape.Save(w)
	if err != nil {
		panic(err)
	}

	w.Flush()
}
*/
