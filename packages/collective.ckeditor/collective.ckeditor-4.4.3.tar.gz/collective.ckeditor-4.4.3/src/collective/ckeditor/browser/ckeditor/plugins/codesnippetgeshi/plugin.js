﻿/*
 Copyright (c) 2003-2015, CKSource - Frederico Knabben. All rights reserved.
 For licensing, see LICENSE.md or http://ckeditor.com/license
*/
(function(){CKEDITOR.plugins.add("codesnippetgeshi",{requires:"ajax,codesnippet",init:function(c){var d=new CKEDITOR.htmlParser.basicWriter,f=new CKEDITOR.plugins.codesnippet.highlighter({languages:a,highlighter:function(b,a,e){b=JSON.stringify({lang:a,html:b});CKEDITOR.ajax.post(CKEDITOR.getUrl(c.config.codeSnippetGeshi_url||""),b,"application/json",function(a){a?(CKEDITOR.htmlParser.fragment.fromHtml(a||"").children[0].writeChildrenHtml(d),e(d.getHtml(!0))):e("")})}});c.plugins.codesnippet.setHighlighter(f)}});
var a={abap:"ABAP",actionscript:"ActionScript",ada:"Ada",apache:"Apache Configuration",applescript:"AppleScript",asm:"Assembly",asp:"Active Server Pages (ASP)",autoit:"AutoIt",bash:"Bash",basic4gl:"Basic4GL",bf:"Brainfuck",blitzbasic:"Blitz BASIC",bnf:"Backus-Naur Form",c:"C",c_mac:"C (Mac)",caddcl:"AutoCAD DCL",cadlisp:"AutoLISP",cfdg:"CFDG",cfm:"ColdFusion Markup Language",cil:"Common Intermediate Language (CIL)",cobol:"COBOL","cpp-qt":"C++ (Qt toolkit)",cpp:"C++",csharp:"C#",css:"Cascading Style Sheets (CSS)",
d:"D",delphi:"Delphi",diff:"Diff",div:"DIV",dos:"DOS batch file",dot:"DOT",eiffel:"Eiffel",fortran:"Fortran",freebasic:"FreeBASIC",gambas:"Gambas",genero:"Genero",gettext:"GNU internationalization (i18n) library",glsl:"OpenGL Shading Language (GLSL)",gml:"Game Maker Language (GML)",gnuplot:"gnuplot",groovy:"Groovy",haskell:"Haskell",hq9plus:"HQ9+",html4strict:"HTML",html5:"HTML5",idl:"Uno IDL",ini:"INI",inno:"Inno",intercal:"INTERCAL",io:"Io",java:"Java",java5:"Java(TM) 2 Platform Standard Edition 5.0",
javascript:"JavaScript",kixtart:"KiXtart",klonec:"Klone C",klonecpp:"Klone C++",latex:"LaTeX",lisp:"Lisp",lolcode:"LOLCODE",lotusscript:"LotusScript",lua:"Lua",Code:"Language",m68k:"Motorola 68000 Assembler",make:"make",matlab:"MATLAB M",mirc:"mIRC scripting language",mxml:"MXML",mpasm:"Microchip Assembler",mysql:"MySQL",nsis:"Nullsoft Scriptable Install System (NSIS)",objc:"Objective-C","ocaml-brief":"OCaml",ocaml:"OCaml",oobas:"OpenOffice.org Basic",oracle8:"Oracle 8 SQL",oracle11:"Oracle 11 SQL",
pascal:"Pascal",per:"per",perl:"Perl","php-brief":"PHP",php:"PHP",pixelbender:"Pixel Bender",plsql:"PL/SQL",povray:"Persistence of Vision Raytracer",powershell:"Windows PowerShell",progress:"OpenEdge Advanced Business Language",prolog:"Prolog",providex:"ProvideX",python:"Python",qbasic:"QBasic/QuickBASIC",rails:"Rails",reg:"Windows Registry",robots:"robots.txt",rsplus:"R",ruby:"Ruby",sas:"SAS",scala:"Scala",scheme:"Scheme",scilab:"Scilab",sdlbasic:"SdlBasic",smalltalk:"Smalltalk",smarty:"Smarty",
sql:"SQL",tcl:"Tcl",teraterm:"Tera Term",text:"Plain text",thinbasic:"thinBasic",tsql:"Transact-SQL",typoscript:"TypoScript",vala:"Vala",vb:"Visual Basic",vbnet:"Visual Basic .NET",verilog:"Verilog",vhdl:"VHDL",vim:"Vimscript",visualfoxpro:"Visual FoxPro",visualprolog:"Visual Prolog",whitespace:"Whitespace",winbatch:"Winbatch",xml:"XML",xorg_conf:"Xorg.conf",xpp:"X++",z80:"ZiLOG Z80 Assembler"}})();