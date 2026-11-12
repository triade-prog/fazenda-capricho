class_name Shapes
extends RefCounted
## Formas desenhadas por código (coração, estrela, curvas), usadas no cenário e nos objetos.


static func heart(size: float, center: Vector2 = Vector2.ZERO, steps: int = 40) -> PackedVector2Array:
	var pts := PackedVector2Array()
	var k := size / 17.0
	for i in steps:
		var t := TAU * i / steps
		var x := 16.0 * pow(sin(t), 3)
		var y := 13.0 * cos(t) - 5.0 * cos(2.0 * t) - 2.0 * cos(3.0 * t) - cos(4.0 * t)
		pts.append(center + Vector2(x, -y) * k)
	return pts


static func star(size: float, center: Vector2 = Vector2.ZERO, points: int = 5) -> PackedVector2Array:
	var pts := PackedVector2Array()
	for i in points * 2:
		var r := size if i % 2 == 0 else size * 0.45
		var a := -PI / 2.0 + PI * i / points
		pts.append(center + Vector2(cos(a), sin(a)) * r)
	return pts


static func ellipse(center: Vector2, radii: Vector2, steps: int = 48) -> PackedVector2Array:
	var pts := PackedVector2Array()
	for i in steps:
		var a := TAU * i / steps
		pts.append(center + Vector2(cos(a) * radii.x, sin(a) * radii.y))
	return pts


static func bezier(p0: Vector2, p1: Vector2, p2: Vector2, t: float) -> Vector2:
	var u := 1.0 - t
	return u * u * p0 + 2.0 * u * t * p1 + t * t * p2


static func closed(pts: PackedVector2Array) -> PackedVector2Array:
	var out := pts.duplicate()
	out.append(pts[0])
	return out
