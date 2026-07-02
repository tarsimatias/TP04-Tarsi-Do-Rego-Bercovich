namespace tp04.Models;
using Microsoft.Data.SqlClient;
using Dapper;
using tp04.Models;

public class bd
{       

private string _connectionString = @"Server=localhost;
DataBase=Album Virtual;Integrated Security=True;TrustServerCertificate=True;";

public List<Figurita> ObtenerFiguritas()
    {
        List<Figurita> Figurita = new List <Figurita>();
        using(SqlConnection connection = new SqlConnection(_connectionString)){
            string query = "SELECT * FROM Figurita";
            Figurita = connection.Query<Figurita>(query).ToList();
        }
        return Figurita;

    }

    public List<Figurita> ObtenerSobre()
    {
//esto agarra la lista de figus, y crea una lista vacia. despues agarra una figu random y la agrega a la lista vacia, y lo repite 5 veces. 
//retorna una lista de 5 figus random. 
        List<Figurita> todasfigus = ObtenerFiguritas();
        List<Figurita> SobreFigus = new List<Figurita>();
        for (int i = 0; i < 5; i++)
        {
            int random = Random.Shared.Next(todasfigus.Count);
            SobreFigus.Add(todasfigus[random]);
        }
        return SobreFigus;
    }



}