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

}