grammar Obsolescence;

obsolescence                : model=modelSet ':' obsolescenceDeclaration+;

obsolescenceDeclaration     : name=ID '(' 'criticality' '=' criticalityType ',' 
                              'confidence' '=' INT ','
                              'date' '=' date=dateObsolescence ')'
                              (temporal=temporalDeclaration | data=dataDeclaration | internal=internalDeclaration )? '{'
                              'impacts:' impact+
                              '}'
                              ;

impact                      : '->' 'elements' '=' modelElement+
                                   'impact' '=' INT '%'
                                   'propagation level' '=' INT
                                   'propagation impact loss' '=' INT '%'
                              ;

temporalDeclaration         : 'expires' '=' (fixed=dateReached | periodic=dateRecurring) ;

internalDeclaration         : 'rule' '=' STRING ;

dataDeclaration             : 'discrepancy' '=' INT;

dateReached                 : 'until' until=dateObsolescence ;

dateRecurring               : 'every' every=periodObsolescence ;

dateObsolescence            : INT '/' INT '/' INT ;

periodObsolescence          : INT tUnit ;

modelElement                : attribute | relation | class | modelSet | functionSet | enumeration ;

attribute                   : 'Attribute' ID 'ofClass' ID ;

relation                    : 'Relation' ID ;

class                       : 'Class' ID ;

modelSet                    : 'Model' ID ;

functionSet                 : 'Function' ID '()' ;

enumeration                 : 'Enumeration' ID ;

criticalityType             : 'Warning' | 'Error' ;

tUnit                       : 's' | 'min' | 'h' | 'd' | 'm' | 'y' ;

WS                          : [ \t\r\n]+ -> skip ;

ML_COMMENT                  : '/*' .*? '*/' -> skip ;

SL_COMMENT                  : '//' ~[\r\n]* -> skip ;

INT                         : [0-9]+ ;

ID                          : [a-zA-Z_][a-zA-Z0-9_]* ;

STRING                      : '"' .*? '"' ;