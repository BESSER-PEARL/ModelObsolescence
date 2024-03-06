# Modeling and Evaluation of model Obsolescence
This repository hosts a DSL (grammar) and a runtime evaluator (implemented in Python) to identify model obsolescence.

Our model-based approach is described in the following figure: at design-time, you can specify how sensitive to obsolescence are the models (using our grammar) and periodically validate (at run-time) the obsolescence of that models and their internal elements.

<img src="/img/approach.png" alt="Approach Overview" style="height: 90%; width:90%;"/>

You can check our mobility case example, including:

* The [mobility domain model](https://github.com/BESSER-PEARL/ModelObsolescence/blob/main/img/mobilitycase.png): this domain model was implemented using [BESSER platform](https://github.com/BESSER-PEARL/BESSER). The implementation of the model is here.
* The [obsolescence rules definition](https://github.com/BESSER-PEARL/ModelObsolescence/blob/main/mobility_case/obsolescence_rules.txt) (using our grammar) applied to the domain model
* An [obsolescence report](https://github.com/BESSER-PEARL/ModelObsolescence/blob/main/mobility_case/report.pdf) generated by the obsolescence evaluator.

## License

This project is licensed under the [MIT](https://mit-license.org/) license.
