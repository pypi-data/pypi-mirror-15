#include "Python.h"
#include "ModernGL.h"

PyObject * InitializeModernGL(PyObject * self, PyObject * args) {
	bool font = true;
	if (!PyArg_ParseTuple(args, "|p:InitializeModernGL", &font)) {
		return 0;
	}
	
	if (ModernGL::InitializeModernGL(font)) {
		Py_RETURN_TRUE;
	} else {
		Py_RETURN_FALSE;
	}
}

PyObject * GetInfo(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":GetInfo")) {
		return 0;
	}

	ModernGL::Info info = ModernGL::GetInfo();
	return Py_BuildValue("IIIss", info.major, info.minor, info.samples, info.vendor, info.renderer);
}

PyObject * GetError(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":GetError")) {
		return 0;
	}

	return PyUnicode_FromString(ModernGL::GetError());
}

PyObject * Viewport(PyObject * self, PyObject * args) {
	int x;
	int y;
	int w;
	int h;

	if (!PyArg_ParseTuple(args, "iiii:Viewport", &x, &y, &w, &h)) {
		return 0;
	}

	ModernGL::Viewport(x, y, w, h);
	Py_RETURN_NONE;
}

PyObject * Clear(PyObject * self, PyObject * args) {
	unsigned char r = 0, g = 0, b = 0, a = 255;

	if (!PyArg_ParseTuple(args, "bbb|b:Clear", &r, &g, &b, &a)) {
		return 0;
	}

	ModernGL::Clear(r, g, b, a);
	Py_RETURN_NONE;
}

PyObject * PointSize(PyObject * self, PyObject * args) {
	float size;

	if (!PyArg_ParseTuple(args, "f:PointSize", &size)) {
		return 0;
	}

	ModernGL::PointSize(size);
	Py_RETURN_NONE;
}

PyObject * LineSize(PyObject * self, PyObject * args) {
	float size;

	if (!PyArg_ParseTuple(args, "f:LineSize", &size)) {
		return 0;
	}

	ModernGL::LineSize(size);
	Py_RETURN_NONE;
}

PyObject * EnableOnly(PyObject * self, PyObject * args) {
	unsigned mask;

	if (!PyArg_ParseTuple(args, "I:EnableOnly", &mask)) {
		return 0;
	}

	ModernGL::EnableOnly(mask);
	Py_RETURN_NONE;
}

PyObject * EnableBlend(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":EnableBlend")) {
		return 0;
	}

	ModernGL::EnableBlend();
	Py_RETURN_NONE;
}

PyObject * DisableBlend(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":DisableBlend")) {
		return 0;
	}

	ModernGL::DisableBlend();
	Py_RETURN_NONE;
}

PyObject * EnableCullFace(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":EnableCullFace")) {
		return 0;
	}

	ModernGL::EnableCullFace();
	Py_RETURN_NONE;
}

PyObject * DisableCullFace(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":DisableCullFace")) {
		return 0;
	}

	ModernGL::DisableCullFace();
	Py_RETURN_NONE;
}

PyObject * EnableDepthTest(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":EnableDepthTest")) {
		return 0;
	}

	ModernGL::EnableDepthTest();
	Py_RETURN_NONE;
}

PyObject * DisableDepthTest(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":DisableDepthTest")) {
		return 0;
	}

	ModernGL::DisableDepthTest();
	Py_RETURN_NONE;
}

PyObject * EnableMultisample(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":EnableMultisample")) {
		return 0;
	}

	ModernGL::EnableMultisample();
	Py_RETURN_NONE;
}

PyObject * DisableMultisample(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":DisableMultisample")) {
		return 0;
	}

	ModernGL::DisableMultisample();
	Py_RETURN_NONE;
}

PyObject * NewFragmentShader(PyObject * self, PyObject * args) {
	const char * source;

	if (!PyArg_ParseTuple(args, "s:NewFragmentShader", &source)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewFragmentShader(source));
}

PyObject * NewGeometryShader(PyObject * self, PyObject * args) {
	const char * source;

	if (!PyArg_ParseTuple(args, "s:NewGeometryShader", &source)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewGeometryShader(source));
}

PyObject * NewVertexShader(PyObject * self, PyObject * args) {
	const char * source;

	if (!PyArg_ParseTuple(args, "s:NewVertexShader", &source)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewVertexShader(source));
}

PyObject * DeleteShader(PyObject * self, PyObject * args) {
	unsigned shader;

	if (!PyArg_ParseTuple(args, "I:DeleteShader", &shader)) {
		return 0;
	}

	ModernGL::DeleteShader(shader);
	Py_RETURN_NONE;
}

PyObject * NewProgram(PyObject * self, PyObject * args) {
	PyObject * lst;

	if (!PyArg_ParseTuple(args, "O:NewProgram", &lst)) {
		return 0;
	}

	int count = PyList_Size(lst);
	unsigned * shader = new unsigned[count];
	for (int i = 0; i < count; ++i) {
		shader[i] = PyLong_AsLong(PyList_GetItem(lst, i));
	}
	unsigned program = ModernGL::NewProgram(shader, count);
	delete[] shader;

	return PyLong_FromLong(program);
}

PyObject * DeleteProgram(PyObject * self, PyObject * args) {
	unsigned program;

	if (!PyArg_ParseTuple(args, "I:DeleteProgram", &program)) {
		return 0;
	}

	ModernGL::DeleteProgram(program);
	Py_RETURN_NONE;
}

PyObject * UseProgram(PyObject * self, PyObject * args) {
	unsigned program;

	if (!PyArg_ParseTuple(args, "I:UseProgram", &program)) {
		return 0;
	}

	ModernGL::UseProgram(program);
	Py_RETURN_NONE;
}

PyObject * UseDefaultProgram(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":UseDefaultProgram")) {
		return 0;
	}

	ModernGL::UseDefaultProgram();
	Py_RETURN_NONE;
}

PyObject * CompilerLog(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":CompilerLog")) {
		return 0;
	}

	return PyUnicode_FromString(ModernGL::CompilerLog());
}

PyObject * AttributeLocation(PyObject * self, PyObject * args) {
	unsigned program;
	const char * name;

	if (!PyArg_ParseTuple(args, "Is:AttributeLocation", &program, &name)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::AttributeLocation(program, name));
}

PyObject * UniformLocation(PyObject * self, PyObject * args) {
	unsigned program;
	const char * name;

	if (!PyArg_ParseTuple(args, "Is:UniformLocation", &program, &name)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::UniformLocation(program, name));
}

PyObject * UniformBlockLocation(PyObject * self, PyObject * args) {
	unsigned program;
	const char * name;

	if (!PyArg_ParseTuple(args, "Is:UniformBlockLocation", &program, &name)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::UniformBlockLocation(program, name));
}

PyObject * Uniform1f(PyObject * self, PyObject * args) {
	unsigned location;
	float v0;

	if (!PyArg_ParseTuple(args, "If:Uniform1f", &location, &v0)) {
		return 0;
	}

	ModernGL::Uniform1f(location, v0);
	Py_RETURN_NONE;
}

PyObject * Uniform2f(PyObject * self, PyObject * args) {
	unsigned location;
	float v0;
	float v1;

	if (!PyArg_ParseTuple(args, "Iff:Uniform2f", &location, &v0, &v1)) {
		return 0;
	}

	ModernGL::Uniform2f(location, v0, v1);
	Py_RETURN_NONE;
}

PyObject * Uniform3f(PyObject * self, PyObject * args) {
	unsigned location;
	float v0;
	float v1;
	float v2;

	if (!PyArg_ParseTuple(args, "Ifff:Uniform3f", &location, &v0, &v1, &v2)) {
		return 0;
	}

	ModernGL::Uniform3f(location, v0, v1, v2);
	Py_RETURN_NONE;
}

PyObject * Uniform4f(PyObject * self, PyObject * args) {
	unsigned location;
	float v0;
	float v1;
	float v2;
	float v3;

	if (!PyArg_ParseTuple(args, "Iffff:Uniform4f", &location, &v0, &v1, &v2, &v3)) {
		return 0;
	}

	ModernGL::Uniform4f(location, v0, v1, v2, v3);
	Py_RETURN_NONE;
}

PyObject * Uniform1i(PyObject * self, PyObject * args) {
	unsigned location;
	int v0;

	if (!PyArg_ParseTuple(args, "Ii:Uniform1i", &location, &v0)) {
		return 0;
	}

	ModernGL::Uniform1i(location, v0);
	Py_RETURN_NONE;
}

PyObject * Uniform2i(PyObject * self, PyObject * args) {
	unsigned location;
	int v0;
	int v1;

	if (!PyArg_ParseTuple(args, "Iii:Uniform2i", &location, &v0, &v1)) {
		return 0;
	}

	ModernGL::Uniform2i(location, v0, v1);
	Py_RETURN_NONE;
}

PyObject * Uniform3i(PyObject * self, PyObject * args) {
	unsigned location;
	int v0;
	int v1;
	int v2;

	if (!PyArg_ParseTuple(args, "Iiii:Uniform3i", &location, &v0, &v1, &v2)) {
		return 0;
	}

	ModernGL::Uniform3i(location, v0, v1, v2);
	Py_RETURN_NONE;
}

PyObject * Uniform4i(PyObject * self, PyObject * args) {
	unsigned location;
	int v0;
	int v1;
	int v2;
	int v3;

	if (!PyArg_ParseTuple(args, "Iiiii:Uniform4i", &location, &v0, &v1, &v2, &v3)) {
		return 0;
	}

	ModernGL::Uniform4i(location, v0, v1, v2, v3);
	Py_RETURN_NONE;
}

PyObject * UniformMatrix(PyObject * self, PyObject * args) {
	unsigned location;
	PyObject * lst;

	if (!PyArg_ParseTuple(args, "IO:UniformMatrix", &location, &lst)) {
		return 0;
	}

	float matrix[16];

	int count = PyList_Size(lst);
	for (int i = 0; i < count; ++i) {
		matrix[i] = PyFloat_AsDouble(PyList_GetItem(lst, i));
	}

	ModernGL::UniformMatrix(location, matrix);
	Py_RETURN_NONE;
}

PyObject * UniformTransposeMatrix(PyObject * self, PyObject * args) {
	unsigned location;
	PyObject * lst;

	if (!PyArg_ParseTuple(args, "IO:UniformTransposeMatrix", &location, &lst)) {
		return 0;
	}

	float matrix[16];

	int count = PyList_Size(lst);
	for (int i = 0; i < count; ++i) {
		matrix[i] = PyFloat_AsDouble(PyList_GetItem(lst, i));
	}

	ModernGL::UniformTransposeMatrix(location, matrix);
	Py_RETURN_NONE;
}

PyObject * UniformBlock(PyObject * self, PyObject * args) {
	unsigned location;
	unsigned buffer;

	if (!PyArg_ParseTuple(args, "II:UniformBlock", &location, &buffer)) {
		return 0;
	}

	ModernGL::UniformBlock(location, buffer);
	Py_RETURN_NONE;
}

PyObject * NewTexture(PyObject * self, PyObject * args) {
	unsigned width;
	unsigned height;
	const void * data;
	unsigned components = 3;
	int size;

	if (!PyArg_ParseTuple(args, "IIy#|I:NewTexture", &width, &height, &data, &size, &components)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewTexture(width, height, data, components));
}

PyObject * DeleteTexture(PyObject * self, PyObject * args) {
	unsigned texture;

	if (!PyArg_ParseTuple(args, "I:DeleteTexture", &texture)) {
		return 0;
	}

	ModernGL::DeleteTexture(texture);
	Py_RETURN_NONE;
}

PyObject * UseTexture(PyObject * self, PyObject * args) {
	unsigned texture;
	unsigned location = 0;

	if (!PyArg_ParseTuple(args, "I|I:UseTexture", &texture, &location)) {
		return 0;
	}

	ModernGL::UseTexture(texture, location);
	Py_RETURN_NONE;
}

PyObject * SetTextureFilter(PyObject * self, PyObject * args) {
	unsigned texture;
	unsigned mode;

	if (!PyArg_ParseTuple(args, "II:SetTextureFilter", &texture, &mode)) {
		return 0;
	}

	ModernGL::SetTextureFilter(texture, mode);
	Py_RETURN_NONE;
}

PyObject * BuildMipmap(PyObject * self, PyObject * args) {
	unsigned texture;
	unsigned base = 0;
	unsigned max = 1000;

	if (!PyArg_ParseTuple(args, "I|II:BuildMipmap", &texture, &base, &max)) {
		return 0;
	}

	ModernGL::BuildMipmap(texture, base, max);
	Py_RETURN_NONE;
}

PyObject * NewVertexArray(PyObject * self, PyObject * args) {
	const char * format;
	PyObject * lst;

	unsigned vertexBuffer;
	unsigned indexBuffer = 0;

	if (!PyArg_ParseTuple(args, "sOI|I:NewVertexArray", &format, &lst, &vertexBuffer, &indexBuffer)) {
		return 0;
	}

	int count = PyList_Size(lst);
	int * attribs = new int[count];
	for (int i = 0; i < count; ++i) {
		attribs[i] = PyLong_AsLong(PyList_GetItem(lst, i));
	}

	PyObject * result = PyLong_FromLong(ModernGL::NewVertexArray(format, attribs, vertexBuffer, indexBuffer));
	delete[] attribs;
	return result;
}

PyObject * DeleteVertexArray(PyObject * self, PyObject * args) {
	unsigned array;

	if (!PyArg_ParseTuple(args, "I:DeleteVertexArray", &array)) {
		return 0;
	}

	ModernGL::DeleteVertexArray(array);
	Py_RETURN_NONE;
}

PyObject * EnableAttribute(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned target;

	if (!PyArg_ParseTuple(args, "II:EnableAttribute", &vao, &target)) {
		return 0;
	}

	ModernGL::EnableAttribute(vao, target);
	Py_RETURN_NONE;
}

PyObject * DisableAttribute(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned target;

	if (!PyArg_ParseTuple(args, "II:DisableAttribute", &vao, &target)) {
		return 0;
	}

	ModernGL::DisableAttribute(vao, target);
	Py_RETURN_NONE;
}

PyObject * EnableAttributes(PyObject * self, PyObject * args) {
	unsigned vao;
	PyObject * attribs;

	if (!PyArg_ParseTuple(args, "IO:EnableAttributes", &vao, &attribs)) {
		return 0;
	}

	int size = PyList_Size(attribs);
	unsigned * attrib_array = new unsigned[size];
	for (int i = 0; i < size; ++i) {
		attrib_array[i] = PyLong_AsLong(PyList_GetItem(attribs, i));
	}
	ModernGL::EnableAttributes(vao, attrib_array, size);
	free(attrib_array);
	Py_RETURN_NONE;
}

PyObject * DisableAttributes(PyObject * self, PyObject * args) {
	unsigned vao;
	PyObject * attribs;

	if (!PyArg_ParseTuple(args, "IO:DisableAttributes", &vao, &attribs)) {
		return 0;
	}

	int size = PyList_Size(attribs);
	unsigned * attrib_array = new unsigned[size];
	for (int i = 0; i < size; ++i) {
		attrib_array[i] = PyLong_AsLong(PyList_GetItem(attribs, i));
	}
	ModernGL::DisableAttributes(vao, attrib_array, size);
	free(attrib_array);
	Py_RETURN_NONE;
}

PyObject * NewVertexBuffer(PyObject * self, PyObject * args) {
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "y#:NewVertexBuffer", &data, &size)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewVertexBuffer(data, size));
}

PyObject * NewIndexBuffer(PyObject * self, PyObject * args) {
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "y#:NewIndexBuffer", &data, &size)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewIndexBuffer(data, size));
}

PyObject * NewUniformBuffer(PyObject * self, PyObject * args) {
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "y#:NewUniformBuffer", &data, &size)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewUniformBuffer(data, size));
}

PyObject * NewDynamicVertexBuffer(PyObject * self, PyObject * args) {
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "y#:NewDynamicVertexBuffer", &data, &size)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewDynamicVertexBuffer(data, size));
}

PyObject * NewDynamicIndexBuffer(PyObject * self, PyObject * args) {
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "y#:NewDynamicIndexBuffer", &data, &size)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewDynamicIndexBuffer(data, size));
}

PyObject * DeleteBuffer(PyObject * self, PyObject * args) {
	unsigned buffer;

	if (!PyArg_ParseTuple(args, "I:DeleteBuffer", &buffer)) {
		return 0;
	}

	ModernGL::DeleteBuffer(buffer);
	Py_RETURN_NONE;
}

PyObject * NewDynamicUniformBuffer(PyObject * self, PyObject * args) {
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "y#:NewDynamicUniformBuffer", &data, &size)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewDynamicUniformBuffer(data, size));
}

PyObject * UpdateVertexBuffer(PyObject * self, PyObject * args) {
	unsigned buffer;
	unsigned offset;
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "IIy#:UpdateVertexBuffer", &buffer, &offset, &data, &size)) {
		return 0;
	}

	ModernGL::UpdateVertexBuffer(buffer, offset, data, size);
	Py_RETURN_NONE;
}

PyObject * UpdateIndexBuffer(PyObject * self, PyObject * args) {
	unsigned buffer;
	unsigned offset;
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "IIy#:UpdateIndexBuffer", &buffer, &offset, &data, &size)) {
		return 0;
	}

	ModernGL::UpdateIndexBuffer(buffer, offset, data, size);
	Py_RETURN_NONE;
}

PyObject * UpdateUniformBuffer(PyObject * self, PyObject * args) {
	unsigned buffer;
	unsigned offset;
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "IIy#:UpdateUniformBuffer", &buffer, &offset, &data, &size)) {
		return 0;
	}

	ModernGL::UpdateUniformBuffer(buffer, offset, data, size);
	Py_RETURN_NONE;
}

PyObject * RenderTriangles(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderTriangles", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderTriangles(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderTriangleStrip(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderTriangleStrip", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderTriangleStrip(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderTriangleFan(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderTriangleFan", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderTriangleFan(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderLines(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderLines", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderLines(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderLineStrip(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderLineStrip", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderLineStrip(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderLineLoop(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderLineLoop", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderLineLoop(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderPoints(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderPoints", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderPoints(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderLineStripAdjacency(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderLineStripAdjacency", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderLineStripAdjacency(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderLinesAdjacency(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderLinesAdjacency", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderLinesAdjacency(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderTriangleStripAdjacency(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderTriangleStripAdjacency", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderTriangleStripAdjacency(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderTrianglesAdjacency(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderTrianglesAdjacency", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderTrianglesAdjacency(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedTriangles(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderIndexedTriangles", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedTriangles(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedTriangleStrip(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderIndexedTriangleStrip", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedTriangleStrip(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedTriangleFan(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderIndexedTriangleFan", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedTriangleFan(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedLines(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderIndexedLines", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedLines(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedLineStrip(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderIndexedLineStrip", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedLineStrip(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedLineLoop(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderIndexedLineLoop", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedLineLoop(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedPoints(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderIndexedPoints", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedPoints(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedLineStripAdjacency(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderIndexedLineStripAdjacency", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedLineStripAdjacency(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedLinesAdjacency(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderIndexedLinesAdjacency", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedLinesAdjacency(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedTriangleStripAdjacency(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderIndexedTriangleStripAdjacency", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedTriangleStripAdjacency(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedTrianglesAdjacency(PyObject * self, PyObject * args) {
	unsigned vao;
	unsigned count;
	unsigned first = 0;
	unsigned instances = 1;

	if (!PyArg_ParseTuple(args, "II|II:RenderIndexedTrianglesAdjacency", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedTrianglesAdjacency(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * NewFramebuffer(PyObject * self, PyObject * args) {
	unsigned width = 0;
	unsigned height = 0;
	bool multisample = true;

	if (!PyArg_ParseTuple(args, "|IIp:NewFramebuffer", &width, &height, &multisample)) {
		return 0;
	}

	ModernGL::Framebuffer framebuffer = ModernGL::NewFramebuffer(width, height, multisample);
	return Py_BuildValue("III", framebuffer.framebuffer, framebuffer.color, framebuffer.depth);
}

PyObject * DeleteFramebuffer(PyObject * self, PyObject * args) {
	unsigned framebuffer;

	if (!PyArg_ParseTuple(args, "I:DeleteFramebuffer", &framebuffer)) {
		return 0;
	}

	ModernGL::DeleteFramebuffer(framebuffer);
	Py_RETURN_NONE;
}

PyObject * UseFramebuffer(PyObject * self, PyObject * args) {
	unsigned framebuffer;

	if (!PyArg_ParseTuple(args, "I:UseFramebuffer", &framebuffer)) {
		return 0;
	}

	ModernGL::UseFramebuffer(framebuffer);
	Py_RETURN_NONE;
}

PyObject * UseDefaultFramebuffer(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":UseDefaultFramebuffer")) {
		return 0;
	}

	ModernGL::UseDefaultFramebuffer();
	Py_RETURN_NONE;
}

PyObject * ReadPixels(PyObject * self, PyObject * args) {
	unsigned x;
	unsigned y;
	unsigned width;
	unsigned height;
	unsigned components = 3;

	if (!PyArg_ParseTuple(args, "IIII|I:ReadPixels", &x, &y, &width, &height, &components)) {
		return 0;
	}

	int size = height * ((width * components + 3) & ~3);
	unsigned char * pixels = ModernGL::ReadPixels(x, y, width, height, components);
	PyObject * data = PyBytes_FromStringAndSize((const char *)pixels, size);
	free(pixels);

	return data;
}

PyObject * ReadDepthPixels(PyObject * self, PyObject * args) {
	unsigned x;
	unsigned y;
	unsigned width;
	unsigned height;
	unsigned components = 3;

	if (!PyArg_ParseTuple(args, "IIII:ReadDepthPixels", &x, &y, &width, &height)) {
		return 0;
	}

	int size = height * height * 4;
	float * pixels = ModernGL::ReadDepthPixels(x, y, width, height);
	PyObject * data = PyBytes_FromStringAndSize((const char *)pixels, size);
	free(pixels);

	return data;
}

PyObject * ReadPixel(PyObject * self, PyObject * args) {
	unsigned x;
	unsigned y;

	if (!PyArg_ParseTuple(args, "II:ReadPixel", &x, &y)) {
		return 0;
	}

	return PyLong_FromUnsignedLong(ModernGL::ReadPixel(x, y));
}

PyObject * ReadDepthPixel(PyObject * self, PyObject * args) {
	unsigned x;
	unsigned y;

	if (!PyArg_ParseTuple(args, "II:ReadDepthPixel", &x, &y)) {
		return 0;
	}

	return PyFloat_FromDouble(ModernGL::ReadDepthPixel(x, y));
}

// OpenGL 4.3+

PyObject * ExtensionActive(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":ExtensionActive")) {
		return 0;
	}

	if (ModernGL::ExtensionActive()) {
		Py_RETURN_TRUE;
	} else {
		Py_RETURN_FALSE;
	}
}

PyObject * NewTessEvaluationShader(PyObject * self, PyObject * args) {
	const char * source;

	if (!PyArg_ParseTuple(args, "s:NewTessEvaluationShader", &source)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewTessEvaluationShader(source));
}

PyObject * NewTessControlShader(PyObject * self, PyObject * args) {
	const char * source;

	if (!PyArg_ParseTuple(args, "s:NewTessControlShader", &source)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewTessControlShader(source));
}

PyObject * NewComputeShader(PyObject * self, PyObject * args) {
	const char * source;

	if (!PyArg_ParseTuple(args, "s:NewComputeShader", &source)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewComputeShader(source));
}

PyObject * DeleteComputeShader(PyObject * self, PyObject * args) {
	unsigned program;

	if (!PyArg_ParseTuple(args, "I:DeleteComputeShader", &program)) {
		return 0;
	}

	ModernGL::DeleteComputeShader(program);
	Py_RETURN_NONE;
}

PyObject * RunComputeShader(PyObject * self, PyObject * args) {
	unsigned program;

	if (!PyArg_ParseTuple(args, "I:RunComputeShader", &program)) {
		return 0;
	}

	ModernGL::RunComputeShader(program);
	Py_RETURN_NONE;
}

PyObject * NewStorageBuffer(PyObject * self, PyObject * args) {
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "y#:NewStorageBuffer", &data, &size)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewStorageBuffer(data, size));
}

PyObject * NewDynamicStorageBuffer(PyObject * self, PyObject * args) {
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "y#:NewDynamicStorageBuffer", &data, &size)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewDynamicStorageBuffer(data, size));
}

PyObject * UpdateStorageBuffer(PyObject * self, PyObject * args) {
	unsigned buffer;
	unsigned offset;
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "IIy#:UpdateStorageBuffer", &buffer, &offset, &data, &size)) {
		return 0;
	}

	ModernGL::UpdateStorageBuffer(buffer, offset, data, size);
	Py_RETURN_NONE;
}

PyObject * UseStorageBuffer(PyObject * self, PyObject * args) {
	unsigned buffer;
	unsigned program;
	unsigned binding = 0;

	if (!PyArg_ParseTuple(args, "II|I:UseStorageBuffer", &buffer, &program, &binding)) {
		return 0;
	}

	ModernGL::UseStorageBuffer(buffer, program, binding);
	Py_RETURN_NONE;
}

PyObject * ReadStorageBuffer(PyObject * self, PyObject * args) {
	unsigned buffer;
	unsigned offset;
	int size;

	if (!PyArg_ParseTuple(args, "IIi:ReadStorageBuffer", &buffer, &offset, &size)) {
		return 0;
	}

	void * content = ModernGL::ReadStorageBuffer(buffer, offset, size);
	PyObject * data = PyBytes_FromStringAndSize((const char *)content, size);
	free(content);

	return data;
}

static PyMethodDef methods[] = {
	{"InitializeModernGL", InitializeModernGL, METH_VARARGS, 0},
	{"GetInfo", GetInfo, METH_VARARGS, 0},
	{"GetError", GetError, METH_VARARGS, 0},

	{"Viewport", Viewport, METH_VARARGS, 0},
	{"Clear", Clear, METH_VARARGS, 0},

	{"PointSize", PointSize, METH_VARARGS, 0},
	{"LineSize", LineSize, METH_VARARGS, 0},

	{"EnableOnly", EnableOnly, METH_VARARGS, 0},
	{"EnableBlend", EnableBlend, METH_VARARGS, 0},
	{"DisableBlend", DisableBlend, METH_VARARGS, 0},
	{"EnableCullFace", EnableCullFace, METH_VARARGS, 0},
	{"DisableCullFace", DisableCullFace, METH_VARARGS, 0},
	{"EnableDepthTest", EnableDepthTest, METH_VARARGS, 0},
	{"DisableDepthTest", DisableDepthTest, METH_VARARGS, 0},
	{"EnableMultisample", EnableMultisample, METH_VARARGS, 0},
	{"DisableMultisample", DisableMultisample, METH_VARARGS, 0},

	{"NewFragmentShader", NewFragmentShader, METH_VARARGS, 0},
	{"NewGeometryShader", NewGeometryShader, METH_VARARGS, 0},
	{"NewVertexShader", NewVertexShader, METH_VARARGS, 0},
	{"DeleteShader", DeleteShader, METH_VARARGS, 0},

	{"NewProgram", NewProgram, METH_VARARGS, 0},
	{"DeleteProgram", DeleteProgram, METH_VARARGS, 0},
	{"UseProgram", UseProgram, METH_VARARGS, 0},
	{"UseDefaultProgram", UseDefaultProgram, METH_VARARGS, 0},

	{"CompilerLog", CompilerLog, METH_VARARGS, 0},

	{"AttributeLocation", AttributeLocation, METH_VARARGS, 0},
	{"UniformLocation", UniformLocation, METH_VARARGS, 0},
	{"UniformBlockLocation", UniformBlockLocation, METH_VARARGS, 0},

	{"Uniform1f", Uniform1f, METH_VARARGS, 0},
	{"Uniform2f", Uniform2f, METH_VARARGS, 0},
	{"Uniform3f", Uniform3f, METH_VARARGS, 0},
	{"Uniform4f", Uniform4f, METH_VARARGS, 0},
	{"Uniform1i", Uniform1i, METH_VARARGS, 0},
	{"Uniform2i", Uniform2i, METH_VARARGS, 0},
	{"Uniform3i", Uniform3i, METH_VARARGS, 0},
	{"Uniform4i", Uniform4i, METH_VARARGS, 0},

	{"UniformMatrix", UniformMatrix, METH_VARARGS, 0},
	{"UniformTransposeMatrix", UniformTransposeMatrix, METH_VARARGS, 0},
	{"UniformBlock", UniformBlock, METH_VARARGS, 0},

	{"NewTexture", NewTexture, METH_VARARGS, 0},
	{"DeleteTexture", DeleteTexture, METH_VARARGS, 0},
	{"UseTexture", UseTexture, METH_VARARGS, 0},

	{"SetTextureFilter", SetTextureFilter, METH_VARARGS, 0},
	{"BuildMipmap", BuildMipmap, METH_VARARGS, 0},

	{"NewVertexArray", NewVertexArray, METH_VARARGS, 0},
	{"DeleteVertexArray", DeleteVertexArray, METH_VARARGS, 0},

	{"EnableAttribute", EnableAttribute, METH_VARARGS, 0},
	{"DisableAttribute", DisableAttribute, METH_VARARGS, 0},
	{"EnableAttributes", EnableAttributes, METH_VARARGS, 0},
	{"DisableAttributes", DisableAttributes, METH_VARARGS, 0},

	{"NewVertexBuffer", NewVertexBuffer, METH_VARARGS, 0},
	{"NewIndexBuffer", NewIndexBuffer, METH_VARARGS, 0},
	{"NewUniformBuffer", NewUniformBuffer, METH_VARARGS, 0},

	{"NewDynamicVertexBuffer", NewDynamicVertexBuffer, METH_VARARGS, 0},
	{"NewDynamicIndexBuffer", NewDynamicIndexBuffer, METH_VARARGS, 0},
	{"NewDynamicUniformBuffer", NewDynamicUniformBuffer, METH_VARARGS, 0},

	{"DeleteBuffer", DeleteBuffer, METH_VARARGS, 0},

	{"UpdateVertexBuffer", UpdateVertexBuffer, METH_VARARGS, 0},
	{"UpdateIndexBuffer", UpdateIndexBuffer, METH_VARARGS, 0},
	{"UpdateUniformBuffer", UpdateUniformBuffer, METH_VARARGS, 0},

	{"RenderTriangles", RenderTriangles, METH_VARARGS, 0},
	{"RenderTriangleStrip", RenderTriangleStrip, METH_VARARGS, 0},
	{"RenderTriangleFan", RenderTriangleFan, METH_VARARGS, 0},
	{"RenderLines", RenderLines, METH_VARARGS, 0},
	{"RenderLineStrip", RenderLineStrip, METH_VARARGS, 0},
	{"RenderLineLoop", RenderLineLoop, METH_VARARGS, 0},
	{"RenderPoints", RenderPoints, METH_VARARGS, 0},
	{"RenderLineStripAdjacency", RenderLineStripAdjacency, METH_VARARGS, 0},
	{"RenderLinesAdjacency", RenderLinesAdjacency, METH_VARARGS, 0},
	{"RenderTriangleStripAdjacency", RenderTriangleStripAdjacency, METH_VARARGS, 0},
	{"RenderTrianglesAdjacency", RenderTrianglesAdjacency, METH_VARARGS, 0},
	{"RenderIndexedTriangles", RenderIndexedTriangles, METH_VARARGS, 0},
	{"RenderIndexedTriangleStrip", RenderIndexedTriangleStrip, METH_VARARGS, 0},
	{"RenderIndexedTriangleFan", RenderIndexedTriangleFan, METH_VARARGS, 0},
	{"RenderIndexedLines", RenderIndexedLines, METH_VARARGS, 0},
	{"RenderIndexedLineStrip", RenderIndexedLineStrip, METH_VARARGS, 0},
	{"RenderIndexedLineLoop", RenderIndexedLineLoop, METH_VARARGS, 0},
	{"RenderIndexedPoints", RenderIndexedPoints, METH_VARARGS, 0},
	{"RenderIndexedLineStripAdjacency", RenderIndexedLineStripAdjacency, METH_VARARGS, 0},
	{"RenderIndexedLinesAdjacency", RenderIndexedLinesAdjacency, METH_VARARGS, 0},
	{"RenderIndexedTriangleStripAdjacency", RenderIndexedTriangleStripAdjacency, METH_VARARGS, 0},
	{"RenderIndexedTrianglesAdjacency", RenderIndexedTrianglesAdjacency, METH_VARARGS, 0},

	{"NewFramebuffer", NewFramebuffer, METH_VARARGS, 0},
	{"DeleteFramebuffer", DeleteFramebuffer, METH_VARARGS, 0},
	{"UseFramebuffer", UseFramebuffer, METH_VARARGS, 0},
	{"UseDefaultFramebuffer", UseDefaultFramebuffer, METH_VARARGS, 0},
	
	{"ReadPixels", ReadPixels, METH_VARARGS, 0},
	{"ReadDepthPixels", ReadDepthPixels, METH_VARARGS, 0},
	{"ReadPixel", ReadPixel, METH_VARARGS, 0},
	{"ReadDepthPixel", ReadDepthPixel, METH_VARARGS, 0},

	// Only OpenGL 4.3+

	{"ExtensionActive", ExtensionActive, METH_VARARGS, 0},
	
	{"NewTessEvaluationShader", NewTessEvaluationShader, METH_VARARGS, 0},
	{"NewTessControlShader", NewTessControlShader, METH_VARARGS, 0},

	{"NewComputeShader", NewComputeShader, METH_VARARGS, 0},
	{"DeleteComputeShader", DeleteComputeShader, METH_VARARGS, 0},
	{"RunComputeShader", RunComputeShader, METH_VARARGS, 0},

	{"NewStorageBuffer", NewStorageBuffer, METH_VARARGS, 0},
	{"NewDynamicStorageBuffer", NewDynamicStorageBuffer, METH_VARARGS, 0},
	{"UseStorageBuffer", UseStorageBuffer, METH_VARARGS, 0},
	{"UpdateStorageBuffer", UpdateStorageBuffer, METH_VARARGS, 0},
	{"ReadStorageBuffer", ReadStorageBuffer, METH_VARARGS, 0},

	// Better than nothing font

	// {"DebugFontColor", DebugFontColor, METH_VARARGS, 0},
	// {"DebugFontAlight", DebugFontAlight, METH_VARARGS, 0},
	// {"DebugFontPrint", DebugFontPrint, METH_VARARGS, 0},

	{0, 0},
};

static struct PyModuleDef moduledef = {PyModuleDef_HEAD_INIT, "ModernGL", 0, -1, methods, 0, 0, 0, 0};

extern "C" {
	PyObject * PyInit_ModernGL();
}

PyObject * PyInit_ModernGL() {
	PyObject * m = PyModule_Create(&moduledef);

	PyModule_AddIntConstant(m, "ENABLE_NOTHING", 0x00);
	PyModule_AddIntConstant(m, "ENABLE_BLEND", 0x01);
	PyModule_AddIntConstant(m, "ENABLE_CULL_FACE", 0x02);
	PyModule_AddIntConstant(m, "ENABLE_DEPTH_TEST", 0x04);
	PyModule_AddIntConstant(m, "ENABLE_MULTISAMPLE", 0x08);

	PyModule_AddIntConstant(m, "TEXTURE_PIXELATED", 0x01);
	PyModule_AddIntConstant(m, "TEXTURE_FILTERED", 0x02);
	PyModule_AddIntConstant(m, "TEXTURE_MIPMAPPED", 0x03);

	PyModule_AddStringConstant(m, "AUTHOR_NAME", "Szabolcs Dombi");
	PyModule_AddStringConstant(m, "AUTHOR_EMAIL", "cprogrammer1994@gmail.com");

	return m;
}
