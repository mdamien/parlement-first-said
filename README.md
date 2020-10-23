# parlement-first-said
*Scripts for @Parl_first_said*

To make it work you need four files in the same directory of the script: `result13.jsonl`, `result14.jsonl`, `result.jsonl` and `result_senat.jsonl`

 - `result.jsonl` is the export of NosDéputés.fr (ND) interventions for the 15th legislature.
 - `result14.jsonl` is the export of NosDéputés.fr interventions for the 14th legislature.
 - `result13.jsonl` is the export of NosDéputés.fr interventions for the 13th legislature.
 - `result_senat.jsonl` is the export of NosSenateurs.fr (NS) interventions.

To get those exports you need:

  - To have this django app that can query the ND/NS dumps: https://github.com/mdamien/nosdeputes-en-django
  - To download the SQL dumps: https://data.regardscitoyens.org/
  - To make it easier, to have a MySQL user `cpc` with a password `password`
  - To ingest those SQL dumps into a different database each time:
      * first `mysql -u cpc -ppassword --default-character-set=utf8 -e "CREATE DATABASE cpc"`
      * then `mysql -u cpc -ppassword --default-character-set=utf8 cpc < donnees.sql`
      * then for ND 14, use `cpc_14` for the database, `cpc_13` for ND 13 and `cpc_senat` for NS
   - Then with the django app, use `python manage.py export_interventions` to get `result.jsonl` on the same directory as the app
       * For `results14.jsonl`, you need to modify the `config/settings.py` with `cpc_14` as the database, same for `result13.jsonl`
       * For `result_senat.jsonl`, you need to switch to the `nossenateurs` branch and then export

You also need:
  
  - `deputes.json` that you can get with `wget nosdeputes.fr/deputes/json -O deputes.json`
  - `senateurs.json` with `wget http://nossenateurs.fr/senateurs/json -O senateurs.json`

Then you can do `python first_said.py`
