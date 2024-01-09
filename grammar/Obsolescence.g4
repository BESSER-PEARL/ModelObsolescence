grammar Obsolescence;

obsolescence                : model=modelSet ':' declarations+=obsolescenceDeclaration+;

obsolescenceDeclaration     : name=ID '(' ('criticality' '=' criticality=criticalityType)? (',' 'confidence' '=' confidence=INT)? 
                              (',' 'date' '=' date=dateObsolescence)? ')'
                              (temporal=temporalDeclaration | data=dataDeclaration | internal=internalDeclaration )? '{'
                              'impacts:' impacts+=impact+
                              '}'
                              ;

impact                      : '->' 'elements:' elements+=modelElement+
                                   'impact:' impact_value=INT
                                   'propagation:' propagation=INT
                                   'impact loss:' impact_loss=INT
                              ;

temporalDeclaration         : 'expires' '=' (fixed=dateReached | periodic=dateRecurring) ;

internalDeclaration         : 'rule' '=' data_rule=STRING ;

dataDeclaration             : 'discrepancy' '=' discrepancy=INT;

dateReached                 : 'until' until=dateObsolescence ;

dateRecurring               : 'every' every=periodObsolescence ;

dateObsolescence            : day=INT '/' month=INT '/' year=INT ;

periodObsolescence          : period=INT tUnit ;

modelElement                : attribute_e=attribute | relation_e=relation | class_e=class | model_e=modelSet | function_e=functionSet ;

attribute                   : 'Attribute' name=ID 'ofClass' class_name=ID ;

relation                    : 'Relation' name=ID ;

class                       : 'Class' name=ID ;

modelSet                    : 'Model' name=ID ;

functionSet                 : 'Function' name=ID '()' ;

criticalityType             : c_type='Warning' | c_type='Error' ;

tUnit                       : 'hour' | 'day' | 'month' | 'year' ;

WS                          : [ \t\r\n]+ -> skip ;

ML_COMMENT                  : '/*' .*? '*/' -> skip ;

SL_COMMENT                  : '//' ~[\r\n]* -> skip ;

INT                         : [0-9]+ ;

ID                          : [a-zA-Z_][a-zA-Z0-9_]* ;

STRING                      : '"' .*? '"' ;