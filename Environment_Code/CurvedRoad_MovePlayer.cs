using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class MovePlayer : MonoBehaviour
{
    public int speed = 15;
    private int i = 0;
    public Text Score;
    public ParticleSystem death;
    void Start()
    {
   
    }
   void OnTriggerEnter(Collider col)
    {
        if (col.gameObject.tag == "Wall")
        {
            SceneManager.LoadScene("GameOver");
        }
        if (col.gameObject.tag == "Finish")
        {
            SceneManager.LoadScene("YouWon");
        }
        if (col.gameObject.tag == "candy")
        {
            Instantiate(death, transform.position, Quaternion.identity);
            i++;
            Score.text = "Score:" + i;
            Destroy(col.gameObject);
        }
    }
    void Update()
    {
        transform.Translate(Vector3.forward * Time.deltaTime * speed);

        if (Input.GetKey(KeyCode.RightArrow))
        {
            Vector3 playerPosition = transform.position;
            playerPosition.x += 0.5f * Time.deltaTime * 22;
            transform.position = playerPosition;
        }

        if (Input.GetKey(KeyCode.LeftArrow))
        {
            Vector3 playerPosition = transform.position;
            playerPosition.x -= 0.5f * Time.deltaTime * 22;
            transform.position = playerPosition;
        }

    }
}
