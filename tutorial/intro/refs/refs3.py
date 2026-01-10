#!/usr/bin/env artisan

from artisan import *

import clang.cindex as ci

print(ci.__file__)

ast = Ast('main.cpp')

var_decls=ast.query("fn{FunctionDecl} => decl{VarDecl}")

if not len(var_decls):
    raise RuntimeError("could not find variable declarations!")

def type_size(t):
    if t.kind in [ci.TypeKind.BOOL, ci.TypeKind.CHAR_U, ci.TypeKind.UCHAR, ci.TypeKind.CHAR_S, ci.TypeKind.SCHAR]:
        return 1
    elif t.kind in [ci.TypeKind.SHORT, ci.TypeKind.USHORT, ]:
        return 2
    elif t.kind in [ci.TypeKind.UINT, ci.TypeKind.INT, ci.TypeKind.FLOAT, ci.TypeKind.ENUM]:
        return 4
    elif t.kind in [ci.TypeKind.LONG, ci.TypeKind.LONGLONG, ci.TypeKind.DOUBLE, ci.TypeKind.POINTER]:
        return 8
    elif t.kind == ci.TypeKind.CONSTANTARRAY:
        return type_size(t.get_array_element_type()) * t.get_array_size()

    elif t.kind == ci.TypeKind.TYPEDEF:
        base_type = ci.conf.lib.clang_getTypedefDeclUnderlyingType(t.get_declaration())
        return type_size(base_type)
        
    elif t.kind in [ci.TypeKind.RECORD, ci.TypeKind.ELABORATED]:

        size = 0
        for f in t.get_fields():
            size = size + type_size(f.type) 
        align = t.get_align()
        return size + (align - size) % align
       
    else:
        raise RuntimeError(f"type {t.spelling} ({t.kind}) not supported!")


for vd in var_decls:
    t = vd.decl.type # class clang.cindex.Type    
    # t.get_size() computes the size internally
    print(f"variable {vd.decl.name} => {type_size(t)} => {t.get_size()}")





