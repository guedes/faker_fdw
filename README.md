# faker_fdw

faker_fdw is a foreign data wrapper for PostgreSQL that generates fake data. 

## How it works?

It's easy, once fake_fdw was installed (see below how to install and create the `faker_srv`), just create 
a foreign table with fields like `ssn`, `name`, `first_name`, `last_name`, `address`, 
`phone_number` and others that you can find [in the providers here](http://fake-factory.readthedocs.org/en/latest/providers.html).

We'll start with `ssn`, `name` and `address`:

```sql
guedes=> CREATE FOREIGN TABLE fake.person (ssn varchar, name varchar, address text) 
         SERVER faker_srv OPTIONS (max_results '100');
CREATE FOREIGN TABLE
Time: 36,400 ms
guedes=> SELECT * FROM fake.person limit 10;
     ssn     |        name        |               address                
-------------+--------------------+--------------------------------------
 452-53-4113 | Jordin McClure PhD | 61875 Bernhard Lights Apt. 594      +
             |                    | Shonnamouth, FL 19690-6384
 586-60-9538 | Isabela D'Amore    | 622 Williamson Road                 +
             |                    | Schmidtside, MH 44962
 525-45-7125 | Irving Terry       | 30478 Cummings Turnpike             +
             |                    | New Chazstad, SC 67727-1963
 314-36-1089 | Janette Bradtke    | 73775 Janell Bridge Apt. 120        +
             |                    | Lonzofort, MH 88220
 382-65-0182 | Dayna Lesch        | 71914 Mosciski Fords                +
             |                    | Lake Dalechester, FM 08869-8100
 698-15-6164 | Judie Dickens      | 7634 Leuschke Burgs                 +
             |                    | West Antonio, MD 76638-0668
 870-44-9100 | Brooks Stroman     | 63236 Pfannerstill Junction Apt. 308+
             |                    | South Shea, MS 34801-5187
 652-43-1400 | Kendrick Denesik   | 0077 Runolfsdottir Cape             +
             |                    | Lake Gaynell, RI 42511
 879-63-4746 | Osie Kemmer        | 4343 Jazlynn Knoll                  +
             |                    | Lake Trueport, AL 88273
 837-30-7043 | Nyasia Smitham     | 3043 Gretta Shoal                   +
             |                    | New Haiden, UT 08099-9192
(10 rows)

Time: 17,276 ms
```

Now, lets suppose that you want the `phone_number`, that's easy, just add
the column:

```sql
guedes=> ALTER FOREIGN TABLE fake.person ADD COLUMN phone_number varchar;
ALTER FOREIGN TABLE
Time: 31,200 ms
guedes=> SELECT * FROM fake.person LIMIT 10;
     ssn     |          name           |            address             |    phone_number    
-------------+-------------------------+--------------------------------+--------------------
 520-61-0046 | Miss Nan Hilll DDS      | 1162 Jaron Mill Apt. 435      +| 635.024.1809x351
             |                         | East Isham, UT 99699-8045      | 
 554-47-6145 | Ayden Jenkins DVM       | 41357 McKenzie Skyway         +| 528.396.8357
             |                         | Port Warren, NM 35237          | 
 021-55-5151 | Dr. Randolf McClure PhD | 9738 Prince Corners Suite 091 +| 696.074.2586x2173
             |                         | Harmonhaven, AK 67018          | 
 441-09-6518 | Harlene Hoppe           | 858 Lenard Port               +| 07969004580
             |                         | Kristinafurt, GU 59690         | 
 486-27-1135 | Dr. Amalie Parker       | 5581 Feil Summit Apt. 736     +| 00554249871
             |                         | West Tatiahaven, PR 12346-7661 | 
 681-31-4609 | Louis Aufderhar I       | 216 Hessel Valley Apt. 891    +| (818)010-0501x1646
             |                         | North Dorothea, RI 12275-4420  | 
 419-81-4064 | Lila Koch DVM           | 354 Fay Vista Suite 603       +| 907-143-1119
             |                         | Greenfelderburgh, MI 50297     | 
 308-50-3314 | Toby Shields            | 059 Nitzsche Parks            +| 383.998.7283x035
             |                         | East Daunte, VT 76481          | 
 405-92-2887 | Delwin Lynch            | 467 Carrol Stream Apt. 466    +| +94(9)7970982195
             |                         | Corimouth, AS 08861            | 
 651-62-6328 | Shantell Pfeffer DVM    | 60971 Nya Villages Suite 939  +| 599.631.2393
             |                         | Mamiestad, GU 54537-9334       | 
(10 rows)

Time: 19,201 ms
```

## Installing

You must install few dependencies related to PostgreSQL and 
Python: `multicorn`, `fake-factory` then `fake_fdw`.

In Debian this is as easy as:

```bash
sudo apt-get install postgresql-9.5-python-multicorn
sudo pip install fake-factory
sudo pip install http://github.com/guedes/faker_fdw/archive/master.zip
```

Once installed, choose which database you want it installed and then:

```sql
CREATE EXTENSION multicorn;
CREATE SERVER faker_srv 
 FOREIGN DATA WRAPPER multicorn
 OPTIONS (wrapper 'faker_fdw.FakerForeignDataWrapper');
```

And that's it! Have fun!

## TODO

1. create a faker_fdw in C;
2. extend examples and documentation;
3. create an entire fake schema that return data with integrity between tables, as fake constraints;
4. ...

# License

faker_fdw is release under PostgreSQL License.

See [LICENSE](LICENSE) file for information.
